# Model Card: GridSense

## Status
Research-stage two-stage community-report modelling prototype for Addis Ababa.

## Stage 1 model
- Target: community outage-report capture risk by sub-city time window
- Dataset: `data/processed/gridsense_forecasting_dataset.csv`
- Features: sub-city, day of week, hour block / time window
- Output: probability-based community-reported outage risk signal

## Stage 2 model
- Scope: reported outage windows/events
- Targets: likely severity and likely duration
- Purpose: prioritize reported outages for local attention

## Intended use
Local planning and awareness support for residents, students, and small businesses.

## Not intended for
Official utility dispatching, emergency response, or regulatory reliability reporting.
