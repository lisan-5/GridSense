from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = ROOT / "data/processed/community_outage_reports_clean.csv"
OUT_PATH = ROOT / "data/processed/gridsense_forecasting_dataset.csv"
SUMMARY_PATH = ROOT / "reports/tables/forecasting_dataset_summary.json"


def block_start(hour: int) -> int:
    return (hour // 3) * 3


def block_label(start_hour: int) -> str:
    end = (start_hour + 3) % 24
    return f"{start_hour:02d}:00-{end:02d}:00"


def mode_or_unknown(series: pd.Series) -> str:
    s = series.dropna().astype(str).str.strip()
    if s.empty:
        return "unknown"
    m = s.mode()
    return m.iloc[0] if not m.empty else "unknown"


def main() -> None:
    df = pd.read_csv(SRC_PATH)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["duration_hours"] = pd.to_numeric(df["duration_hours"], errors="coerce")
    df["confidence_score"] = pd.to_numeric(df["confidence_score"], errors="coerce")

    for col in ["sub_city", "sefer_or_landmark", "weather_condition", "impact_level", "planned_notice"]:
        df[col] = df[col].astype(str).str.strip().str.lower()

    start_dt = pd.to_datetime(
        df["date"].dt.strftime("%Y-%m-%d") + " " + df["outage_start_time"].astype(str),
        errors="coerce",
    )
    df["hour"] = start_dt.dt.hour.fillna(0).astype(int)
    df["hour_block_start"] = df["hour"].apply(block_start)
    df["time_window"] = df["hour_block_start"].apply(block_label)
    df["day_of_week"] = df["date"].dt.day_name().fillna("Unknown")
    df["is_rainy"] = df["weather_condition"].str.contains("rain|storm", case=False, na=False).astype(int)

    # Proxy outage label at report row level to support forecasting window aggregation.
    df["outage_proxy"] = (
        (df["duration_hours"] > 1.0) | (df["impact_level"].isin(["medium", "high", "critical"]))
    ).astype(int)
    df["high_severity_proxy"] = (
        (df["duration_hours"] >= 2.5) | (df["impact_level"].isin(["high", "critical"]))
    ).astype(int)

    # Aggregate observed rows to sub_city x date x 3-hour window.
    grp_cols = ["date", "sub_city", "hour_block_start", "time_window", "day_of_week"]
    agg = (
        df.groupby(grp_cols, dropna=False)
        .agg(
            reports_count=("outage_proxy", "size"),
            outage_occurred=("outage_proxy", "max"),
            avg_duration_hours=("duration_hours", "mean"),
            max_duration_hours=("duration_hours", "max"),
            high_severity_outage=("high_severity_proxy", "max"),
            weather_condition=("weather_condition", mode_or_unknown),
            is_rainy=("is_rainy", "max"),
            planned_notice_mode=("planned_notice", mode_or_unknown),
            representative_sefer=("sefer_or_landmark", mode_or_unknown),
            confidence_score_mean=("confidence_score", "mean"),
        )
        .reset_index()
    )

    # Create full grid for no-report/no-outage windows.
    dates = sorted(agg["date"].dropna().unique())
    sub_cities = sorted(agg["sub_city"].dropna().unique())
    blocks = sorted(agg["hour_block_start"].dropna().unique())
    full = pd.MultiIndex.from_product(
        [dates, sub_cities, blocks], names=["date", "sub_city", "hour_block_start"]
    ).to_frame(index=False)
    full["time_window"] = full["hour_block_start"].apply(block_label)
    full["day_of_week"] = pd.to_datetime(full["date"]).dt.day_name()

    merged = full.merge(
        agg,
        on=["date", "sub_city", "hour_block_start", "time_window", "day_of_week"],
        how="left",
    )

    merged["reports_count"] = merged["reports_count"].fillna(0).astype(int)
    merged["outage_occurred"] = merged["outage_occurred"].fillna(0).astype(int)
    merged["high_severity_outage"] = merged["high_severity_outage"].fillna(0).astype(int)
    merged["avg_duration_hours"] = merged["avg_duration_hours"].fillna(0.0)
    merged["max_duration_hours"] = merged["max_duration_hours"].fillna(0.0)
    merged["weather_condition"] = merged["weather_condition"].fillna("unknown")
    merged["is_rainy"] = merged["is_rainy"].fillna(0).astype(int)
    merged["planned_notice_mode"] = merged["planned_notice_mode"].fillna("unknown")
    merged["representative_sefer"] = merged["representative_sefer"].fillna("unknown")
    merged["confidence_score_mean"] = merged["confidence_score_mean"].fillna(0.0)
    merged["respondents_count_proxy"] = merged["reports_count"]

    merged["date"] = pd.to_datetime(merged["date"]).dt.strftime("%Y-%m-%d")
    merged = merged.sort_values(["date", "sub_city", "hour_block_start"]).reset_index(drop=True)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(OUT_PATH, index=False)

    summary = {
        "rows": int(len(merged)),
        "outage_occurred_counts": merged["outage_occurred"].value_counts().to_dict(),
        "high_severity_outage_counts": merged["high_severity_outage"].value_counts().to_dict(),
        "sub_city_count": int(merged["sub_city"].nunique()),
        "date_count": int(merged["date"].nunique()),
        "time_windows": sorted(merged["time_window"].unique().tolist()),
    }
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
