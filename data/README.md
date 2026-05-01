# Data notes

Primary analysis dataset:
- `processed/gridsense_forecasting_dataset.csv`

Supporting datasets:
- `processed/community_outage_reports_clean.csv`
- `collected/community_outage_reports.csv`
- `processed/local_evidence_dataset.csv`
- `raw/*` source/context files

Workflow:
1. Collect anonymous community reports (`collected/`)
2. Clean event-level data (`processed/community_outage_reports_clean.csv`)
3. Build forecasting windows (`processed/gridsense_forecasting_dataset.csv`)
4. Train two-stage models (`src/train_two_stage_models.py`)
