# Dataset Description

The dataset contains anonymous community-reported electricity outage records from Addis Ababa.

## Privacy

The public dataset excludes:
- names
- phone numbers
- emails
- exact addresses
- GPS coordinates
- free-text notes

## Main file

`data/processed/community_outage_reports_clean.csv`

## Columns

| Column | Description |
|---|---|
| report_id | Anonymous report identifier |
| date | Date of reported outage |
| sub_city | Addis Ababa sub-city |
| sefer_or_landmark | General area/landmark, not exact address |
| outage_start_time | Approximate outage start time |
| outage_end_time | Approximate outage end time |
| duration_hours | Estimated outage duration |
| planned_notice | Whether respondent knew it was planned |
| impact_level | Low, medium, or high reported impact |
| weather_condition | Reported weather condition |
| source_type | Collection channel label |
| confidence_score | Data confidence score |
| high_risk_outage | Research label for high-risk outage |
