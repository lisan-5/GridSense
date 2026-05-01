from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    precision_score,
    precision_recall_curve,
    r2_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data/processed/gridsense_forecasting_dataset.csv"
OUT_PATH = ROOT / "reports/tables/two_stage_model_metrics.json"


def classification_metrics(name: str, y_true, y_pred, y_prob) -> dict:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return {
        "model": name,
        "accuracy": round(accuracy_score(y_true, y_pred), 4),
        "balanced_accuracy": round(balanced_accuracy_score(y_true, y_pred), 4),
        "precision": round(precision_score(y_true, y_pred, zero_division=0), 4),
        "recall": round(recall_score(y_true, y_pred, zero_division=0), 4),
        "f1": round(f1_score(y_true, y_pred, zero_division=0), 4),
        "roc_auc": round(roc_auc_score(y_true, y_prob), 4),
        "pr_auc": round(average_precision_score(y_true, y_prob), 4),
        "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
    }


def best_f1_threshold(y_true, y_prob) -> float:
    p, r, t = precision_recall_curve(y_true, y_prob)
    f1 = (2 * p * r) / (p + r + 1e-12)
    if len(t) == 0:
        return 0.5
    idx = int(np.nanargmax(f1[:-1]))
    return float(t[idx])


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["is_weekend"] = df["day_of_week"].isin(["Saturday", "Sunday"]).astype(int)
    df = df.sort_values(["sub_city", "hour_block_start", "date"]).reset_index(drop=True)
    grp = df.groupby(["sub_city", "hour_block_start"], dropna=False)
    df["lag1_outage_reported"] = grp["outage_reported"].shift(1).fillna(0).astype(int)
    df["rolling3_report_rate"] = grp["outage_reported"].transform(
        lambda s: s.shift(1).rolling(window=3, min_periods=1).mean()
    ).fillna(0.0)
    df["hour_sin"] = np.sin(2 * np.pi * df["hour_block_start"] / 24.0)
    df["hour_cos"] = np.cos(2 * np.pi * df["hour_block_start"] / 24.0)

    # Stage 1: community outage-report risk forecasting
    stage1_features = [
        "hour_block_start",
        "hour_sin",
        "hour_cos",
        "day_of_week",
        "is_weekend",
        "sub_city",
        "lag1_outage_reported",
        "rolling3_report_rate",
    ]
    X1 = df[stage1_features].copy()
    y1 = df["outage_reported"].astype(int)

    num1 = [
        "hour_block_start",
        "hour_sin",
        "hour_cos",
        "is_weekend",
        "lag1_outage_reported",
        "rolling3_report_rate",
    ]
    cat1 = ["day_of_week", "sub_city"]
    prep1 = ColumnTransformer(
        [
            ("num", Pipeline([("imp", SimpleImputer(strategy="median"))]), num1),
            (
                "cat",
                Pipeline(
                    [("imp", SimpleImputer(strategy="most_frequent")), ("oh", OneHotEncoder(handle_unknown="ignore"))]
                ),
                cat1,
            ),
        ]
    )

    split_date = df["date"].dropna().quantile(0.75)
    train_mask = df["date"] <= split_date
    X1_train, X1_test = X1[train_mask], X1[~train_mask]
    y1_train, y1_test = y1[train_mask], y1[~train_mask]

    stage1_models = {
        "dummy_baseline": DummyClassifier(strategy="most_frequent"),
        "logistic_regression": LogisticRegression(max_iter=3000, class_weight="balanced", random_state=42),
        "random_forest": RandomForestClassifier(
            n_estimators=600, min_samples_leaf=2, class_weight="balanced_subsample", random_state=42
        ),
    }
    stage1_results = []
    for name, model in stage1_models.items():
        pipe = Pipeline([("prep", prep1), ("model", model)])
        pipe.fit(X1_train, y1_train)
        y_prob = pipe.predict_proba(X1_test)[:, 1] if hasattr(pipe, "predict_proba") else y1_test.to_numpy()
        if name == "dummy_baseline":
            y_pred = pipe.predict(X1_test)
            threshold = 0.5
        else:
            train_prob = pipe.predict_proba(X1_train)[:, 1]
            threshold = best_f1_threshold(y1_train, train_prob)
            y_pred = (y_prob >= threshold).astype(int)
        m = classification_metrics(name, y1_test, y_pred, y_prob)
        m["threshold"] = round(float(threshold), 4)
        stage1_results.append(m)

    # Stage 2: conditional models on outage rows only
    outage_df = df[df["outage_reported"] == 1].copy()
    stage2_features = [
        "hour_block_start",
        "sub_city",
        "weather_condition",
        "planned_notice_mode",
        "confidence_score_mean",
    ]
    X2 = outage_df[stage2_features].copy()

    num2 = ["hour_block_start", "confidence_score_mean"]
    cat2 = ["sub_city", "weather_condition", "planned_notice_mode"]
    prep2 = ColumnTransformer(
        [
            ("num", Pipeline([("imp", SimpleImputer(strategy="median"))]), num2),
            (
                "cat",
                Pipeline(
                    [("imp", SimpleImputer(strategy="most_frequent")), ("oh", OneHotEncoder(handle_unknown="ignore"))]
                ),
                cat2,
            ),
        ]
    )

    # 2a: high_severity_outage classification
    y2_cls = outage_df["high_severity_outage"].astype(int)
    X2_train, X2_test, y2_train, y2_test = train_test_split(
        X2, y2_cls, test_size=0.25, random_state=42, stratify=y2_cls
    )
    cls_pipe = Pipeline(
        [
            ("prep", prep2),
            (
                "model",
                RandomForestClassifier(
                    n_estimators=300, min_samples_leaf=2, class_weight="balanced", random_state=42
                ),
            ),
        ]
    )
    cls_pipe.fit(X2_train, y2_train)
    y2_pred = cls_pipe.predict(X2_test)
    y2_prob = cls_pipe.predict_proba(X2_test)[:, 1]
    stage2_cls = classification_metrics("random_forest_high_severity", y2_test, y2_pred, y2_prob)

    # 2b: duration regression
    y2_reg = outage_df["avg_duration_hours"].astype(float)
    Xr_train, Xr_test, yr_train, yr_test = train_test_split(X2, y2_reg, test_size=0.25, random_state=42)
    reg_pipe = Pipeline([("prep", prep2), ("model", RandomForestRegressor(n_estimators=300, random_state=42))])
    reg_pipe.fit(Xr_train, yr_train)
    yr_pred = reg_pipe.predict(Xr_test)
    stage2_reg = {
        "model": "random_forest_duration_regressor",
        "mae": round(mean_absolute_error(yr_test, yr_pred), 4),
        "r2": round(r2_score(yr_test, yr_pred), 4),
    }

    results = {
        "dataset_rows": int(len(df)),
        "stage1_outage_forecasting": {
            "target": "outage_reported",
            "features": stage1_features,
            "split": {
                "type": "time_based",
                "train_end_date": pd.to_datetime(split_date).strftime("%Y-%m-%d"),
                "train_rows": int(train_mask.sum()),
                "test_rows": int((~train_mask).sum()),
            },
            "class_balance": df["outage_reported"].value_counts().to_dict(),
            "models": stage1_results,
        },
        "stage2_conditional_models": {
            "scope": "rows where outage_reported == 1",
            "rows": int(len(outage_df)),
            "features": stage2_features,
            "severity_classifier": stage2_cls,
            "duration_regressor": stage2_reg,
        },
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
