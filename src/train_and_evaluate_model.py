from __future__ import annotations

import csv
import json
from pathlib import Path

from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data/processed/community_outage_reports_clean.csv"
OUT_PATH = ROOT / "reports/tables/model_metrics.json"


def read_rows(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def to_float(value: str, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def build_dataset(rows: list[dict]) -> tuple[list[dict], list[int]]:
    xs: list[dict] = []
    ys: list[int] = []
    for r in rows:
        target_raw = (r.get("high_risk_outage") or "").strip()
        if target_raw in {"0", "1"}:
            y = int(target_raw)
        else:
            duration = to_float(r.get("duration_hours"), 0.0)
            impact = (r.get("impact_level") or "").strip().lower()
            y = 1 if duration >= 2.0 or impact in {"high", "critical"} else 0

        start_time = (r.get("outage_start_time") or "00:00").strip()
        hour = 0
        try:
            hour = int(start_time.split(":")[0])
        except Exception:
            pass

        x = {
            "start_hour": hour,
            "sub_city": (r.get("sub_city") or "unknown").strip(),
            "planned_notice": (r.get("planned_notice") or "unknown").strip(),
            "weather_condition": (r.get("weather_condition") or "unknown").strip(),
            "source_type": (r.get("source_type") or "unknown").strip(),
            "confidence_score": to_float(r.get("confidence_score"), 0.0),
        }
        xs.append(x)
        ys.append(y)
    return xs, ys


def evaluate(name: str, model, x_train, y_train, x_test, y_test) -> dict:
    model.fit(x_train, y_train)
    preds = model.predict(x_test)
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(x_test)[:, 1]
    else:
        probs = preds

    tn, fp, fn, tp = confusion_matrix(y_test, preds, labels=[0, 1]).ravel()
    return {
        "model": name,
        "accuracy": round(accuracy_score(y_test, preds), 4),
        "precision_high_risk": round(precision_score(y_test, preds, zero_division=0), 4),
        "recall_high_risk": round(recall_score(y_test, preds, zero_division=0), 4),
        "f1_high_risk": round(f1_score(y_test, preds, zero_division=0), 4),
        "roc_auc": round(roc_auc_score(y_test, probs), 4),
        "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
    }


def main() -> None:
    rows = read_rows(DATA_PATH)
    if len(rows) < 80:
        raise ValueError(f"Need at least 80 rows to evaluate reliably. Found {len(rows)}.")

    xs, ys = build_dataset(rows)
    x_train_rows, x_test_rows, y_train, y_test = train_test_split(
        xs, ys, test_size=0.25, random_state=42, stratify=ys
    )

    vec = DictVectorizer(sparse=False)
    x_train = vec.fit_transform(x_train_rows)
    x_test = vec.transform(x_test_rows)

    metrics = {
        "data_summary": {
            "n_rows": len(rows),
            "train_size": len(y_train),
            "test_size": len(y_test),
            "positive_rate_train": round(sum(y_train) / len(y_train), 4),
            "positive_rate_test": round(sum(y_test) / len(y_test), 4),
            "feature_count_after_encoding": int(x_train.shape[1]),
        },
        "models": [],
    }

    baseline = DummyClassifier(strategy="most_frequent")
    metrics["models"].append(evaluate("dummy_most_frequent", baseline, x_train, y_train, x_test, y_test))

    log_reg = LogisticRegression(max_iter=1000, random_state=42)
    metrics["models"].append(evaluate("logistic_regression", log_reg, x_train, y_train, x_test, y_test))

    forest = RandomForestClassifier(
        n_estimators=300, random_state=42, class_weight="balanced", min_samples_leaf=2
    )
    metrics["models"].append(evaluate("random_forest", forest, x_train, y_train, x_test, y_test))

    best = max(metrics["models"], key=lambda m: m["f1_high_risk"])
    metrics["best_model_by_f1_high_risk"] = best["model"]

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
