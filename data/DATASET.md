# Dataset Description

GridSense uses two related datasets:

1. `data/processed/community_outage_reports_clean.csv`
- Cleaned event-level anonymous community outage reports.

2. `data/processed/gridsense_forecasting_dataset.csv`
- Forecasting-ready window-level dataset (date + sub-city + 3-hour block) with both outage and no-outage windows.

## Privacy

Public datasets exclude:
- names
- phone numbers
- emails
- exact addresses
- GPS coordinates
- free-text notes

## Forecasting dataset columns

| Column | Description |
|---|---|
| date | Date of observation window |
| sub_city | Addis Ababa sub-city |
| hour_block_start | Start hour of 3-hour block |
| time_window | 3-hour window label |
| day_of_week | Day name |
| reports_count | Community report count in window |
| respondents_count_proxy | Proxy participation count |
| outage_reported | Forecasting target (0/1) |
| avg_duration_hours | Mean duration in window |
| max_duration_hours | Maximum duration in window |
| high_severity_outage | Conditional severity target (0/1) |
| weather_condition | Mode weather condition |
| is_rainy | Rain/storm indicator |
| planned_notice_mode | Mode planning-status label |
| representative_sefer | Representative sefer/landmark |
| confidence_score_mean | Mean confidence score |

## Labeling note

`outage_reported` is constructed from aggregated community report evidence at the time-window level. This enables first-step local forecasting but should not be interpreted as official utility outage telemetry.

