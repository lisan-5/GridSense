# Model Card: GridSense

## Status
Research model trained and evaluated on real collected community reports; not production.

## Training data
- File: `data/processed/community_outage_reports_clean.csv` (primary)
- Source intake: `data/collected/community_outage_reports.csv`
- Records used: 198
- Target: `high_risk_outage` (0/1), from collected labels/rules

## Current task
- Classification: `high_risk_outage`.
- Features: start hour, sub-city, planned notice, weather, source type, confidence score.

## Evaluation summary
- Baseline (`most_frequent`): accuracy 0.56, F1-high-risk 0.00.
- Logistic Regression: accuracy 0.78, F1-high-risk 0.7442, ROC-AUC 0.8961.
- Random Forest (best by F1): accuracy 0.80, F1-high-risk 0.7619, ROC-AUC 0.9221.
- Full metrics: `reports/tables/model_metrics.json`.

## Intended use
Planning, exploration, and decision-support research.

## Not intended for
Official outage announcements or emergency decisions.

