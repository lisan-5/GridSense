# Data Card: GridSense

## Data purpose
To investigate electricity reliability in Addis Ababa using public, non-personal evidence and to define a safe path toward future outage-risk modelling.

## Included data
- Addis Ababa reliability baselines and targets.
- Public evidence about outage-related issues and infrastructure upgrades.
- Ethiopia Enterprise Survey outage indicators.
- A non-personal future community report template.
- Processed analysis dataset: `data/processed/community_outage_reports_clean.csv` (current n=198).
- Raw intake dataset: `data/collected/community_outage_reports.csv`.

## Privacy
No personal data is included. The future report template avoids names, phone numbers, exact household addresses, and private identifiers.

## Limitation
The current event-level dataset is useful for research evaluation, but still limited for production-grade deployment. This is treated explicitly in the notebook and model card.

