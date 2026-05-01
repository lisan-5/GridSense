# Model Card: GridSense

## Status
Research-stage two-stage forecasting prototype for Addis Ababa outage risk.

## Stage 1 model
- Target: `outage_reported`
- Dataset: `data/processed/gridsense_forecasting_dataset.csv`
- Features: hour block, day of week, sub-city, weather, rainy flag, planning-status mode
- Models: dummy baseline, logistic regression, random forest

## Stage 2 model
- Scope: rows with `outage_reported = 1`
- Targets: `high_severity_outage` and `avg_duration_hours`
- Features: hour block, sub-city, weather, planning-status mode, confidence score mean

## Intended use
Local planning and awareness support for residents, students, and small businesses.

## Not intended for
Official utility dispatching, emergency response, or regulatory reliability reporting.

