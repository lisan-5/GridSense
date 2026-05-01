import csv
from datetime import date, datetime, time
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
COLLECTED_DIR = ROOT / "data" / "collected"
COLLECTED_PATH = COLLECTED_DIR / "community_outage_reports.csv"
TEMPLATE_PATH = RAW_DIR / "community_report_template_no_personal_data.csv"

FIELDNAMES = [
    "report_id",
    "date",
    "sub_city",
    "sefer_or_landmark",
    "outage_start_time",
    "outage_end_time",
    "duration_hours",
    "planned_notice",
    "impact_level",
    "weather_condition",
    "source_type",
    "confidence_score",
    "notes_without_personal_data",
]

SUB_CITIES = [
    "Addis Ketema",
    "Akaky Kaliti",
    "Arada",
    "Bole",
    "Gullele",
    "Kirkos",
    "Kolfe Keranio",
    "Lideta",
    "Nifas Silk-Lafto",
    "Yeka",
    "Other/Unknown",
]


def ensure_collected_csv() -> None:
    COLLECTED_DIR.mkdir(parents=True, exist_ok=True)
    if not COLLECTED_PATH.exists():
        with open(COLLECTED_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def read_csv_rows(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def append_row(row: dict) -> None:
    with open(COLLECTED_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(row)


def next_report_id(rows: list[dict]) -> str:
    return f"COMM-{len(rows) + 1:05d}"


def to_duration_hours(start_t: time, end_t: time) -> float:
    start_dt = datetime.combine(date.today(), start_t)
    end_dt = datetime.combine(date.today(), end_t)
    if end_dt < start_dt:
        end_dt = end_dt.replace(day=end_dt.day + 1)
    return round((end_dt - start_dt).total_seconds() / 3600.0, 2)


def quality_summary(rows: list[dict]) -> dict:
    if not rows:
        return {"total": 0, "missing_sub_city": 0, "missing_duration": 0, "low_confidence": 0}
    missing_sub_city = sum(1 for r in rows if not r["sub_city"].strip())
    missing_duration = sum(1 for r in rows if not r["duration_hours"].strip())
    low_confidence = sum(1 for r in rows if float(r["confidence_score"] or 0) < 0.5)
    return {
        "total": len(rows),
        "missing_sub_city": missing_sub_city,
        "missing_duration": missing_duration,
        "low_confidence": low_confidence,
    }


ensure_collected_csv()
st.set_page_config(page_title="GridSense", layout="wide")
st.title("GridSense")
st.caption("Real-data-first electricity reliability analysis for Addis Ababa")

st.markdown(
    """
This dashboard now supports **real community evidence collection** with no personal data.
Use the form below to add verified outage reports to a local dataset used by your project.
"""
)

with open(RAW_DIR / "addis_ababa_reliability_context.csv", newline="", encoding="utf-8") as f:
    context = list(csv.DictReader(f))

cols = st.columns(4)
lookup = {r["metric"]: r for r in context}
cols[0].metric("Addis Ababa access", lookup["electricity_access"]["value"] + "%")
cols[1].metric("MV interruptions baseline", lookup["medium_voltage_line_interruptions"]["value"])
cols[2].metric("Interruption hours baseline", lookup["medium_voltage_interruption_duration"]["value"])
cols[3].metric("Issues resolved", lookup["outage_related_problems_resolved"]["value"] + "%")

st.subheader("Add community outage report (non-personal)")
st.info("Do not enter names, phone numbers, exact household addresses, or any personal identifiers.")

existing_rows = read_csv_rows(COLLECTED_PATH)
generated_report_id = next_report_id(existing_rows)

with st.form("community_report_form", clear_on_submit=True):
    c1, c2, c3 = st.columns(3)
    report_date = c1.date_input("Date", value=date.today())
    sub_city = c2.selectbox("Sub-city", options=SUB_CITIES, index=3)
    sefer = c3.text_input("Sefer / landmark (general only)", max_chars=80)

    c4, c5, c6 = st.columns(3)
    start_time = c4.time_input("Outage start time", value=time(9, 0))
    end_time = c5.time_input("Outage end time", value=time(11, 0))
    duration_hours = c6.number_input(
        "Duration (hours) override",
        min_value=0.0,
        max_value=72.0,
        value=0.0,
        step=0.25,
        help="Leave at 0 to auto-calculate from start/end time.",
    )

    c7, c8, c9 = st.columns(3)
    planned_notice = c7.selectbox("Planned notice", options=["yes", "no", "unknown"])
    impact_level = c8.selectbox("Impact level", options=["low", "medium", "high", "critical"])
    weather_condition = c9.selectbox(
        "Weather condition", options=["clear", "cloudy", "light_rain", "heavy_rain", "storm", "unknown"]
    )

    c10, c11 = st.columns(2)
    source_type = c10.selectbox(
        "Source type",
        options=["community_report", "official_notice", "news_report", "field_observation"],
    )
    confidence_score = c11.slider("Confidence score", min_value=0.0, max_value=1.0, value=0.8, step=0.05)

    notes = st.text_area("Notes (non-personal only)", max_chars=240)
    submitted = st.form_submit_button("Save report")

if submitted:
    if "@" in notes or any(token in notes.lower() for token in ["phone", "tel", "name:", "id:", "house number"]):
        st.error("Possible personal data detected in notes. Remove personal details and submit again.")
    else:
        final_duration = round(duration_hours, 2) if duration_hours > 0 else to_duration_hours(start_time, end_time)
        row = {
            "report_id": generated_report_id,
            "date": report_date.isoformat(),
            "sub_city": sub_city,
            "sefer_or_landmark": sefer.strip(),
            "outage_start_time": start_time.strftime("%H:%M"),
            "outage_end_time": end_time.strftime("%H:%M"),
            "duration_hours": f"{final_duration:.2f}",
            "planned_notice": planned_notice,
            "impact_level": impact_level,
            "weather_condition": weather_condition,
            "source_type": source_type,
            "confidence_score": f"{confidence_score:.2f}",
            "notes_without_personal_data": notes.strip(),
        }
        append_row(row)
        st.success(f"Saved report {generated_report_id} to data/collected/community_outage_reports.csv")
        st.rerun()

st.subheader("Collected dataset preview")
rows = read_csv_rows(COLLECTED_PATH)
st.caption(f"Rows collected: {len(rows)}")
st.dataframe(rows, use_container_width=True, height=280)

qs = quality_summary(rows)
q1, q2, q3, q4 = st.columns(4)
q1.metric("Total reports", qs["total"])
q2.metric("Missing sub-city", qs["missing_sub_city"])
q3.metric("Missing duration", qs["missing_duration"])
q4.metric("Low-confidence (<0.50)", qs["low_confidence"])

with open(COLLECTED_PATH, "r", encoding="utf-8") as f:
    st.download_button(
        label="Download collected CSV",
        data=f.read(),
        file_name="community_outage_reports.csv",
        mime="text/csv",
    )

st.subheader("Source evidence context")
st.dataframe(context, use_container_width=True)

st.subheader("Model-ready input schema")
with open(ROOT / "data/raw/model_ready_event_schema.csv", newline="", encoding="utf-8") as f:
    schema = list(csv.DictReader(f))
st.dataframe(schema, use_container_width=True)

