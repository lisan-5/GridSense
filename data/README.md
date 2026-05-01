# Data notes

This version intentionally avoids using synthetic datasets as the main project data.

Included public and collected CSV files:

- `raw/addis_ababa_reliability_context.csv` - official/public reliability evidence for Addis Ababa.
- `raw/ethiopia_enterprise_outage_indicators.csv` - Ethiopia Enterprise Survey indicators related to outages.
- `raw/verified_public_outage_evidence.csv` - a small public evidence log with source URLs.
- `raw/model_ready_event_schema.csv` - the event-level schema used by the project.
- `raw/community_report_template_no_personal_data.csv` - safe report template with no names, phone numbers, exact household addresses, or personal identifiers.
- `collected/community_outage_reports.csv` - raw community-collected outage reports captured via the Streamlit form.
- `processed/community_outage_reports_clean.csv` - cleaned analysis dataset used by the notebook.

Model training/evaluation uses the cleaned processed file via:

- `src/train_and_evaluate_model.py`
- Output metrics: `reports/tables/model_metrics.json`

The notebook separates current evidence-supported conclusions from non-supported operational claims.
