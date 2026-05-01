# GridSense

GridSense is a Kujenga final project focused on **forecasting electricity outage risk in Addis Ababa** using community reports, time, location, planning status, and weather conditions.

The project now uses a two-stage modeling system:
1. **Outage risk forecasting model** (`outage_occurred`).
2. **Conditional impact model** (severity/duration if outage occurs).

## Main notebook

`notebooks/lisanegebriel_ethiopia_final_project.ipynb`

## Dataset

Primary forecasting dataset:
- `data/processed/gridsense_forecasting_dataset.csv`

Supporting datasets:
- `data/processed/community_outage_reports_clean.csv` (clean event-level community reports)
- `data/collected/community_outage_reports.csv` (raw intake)

All public datasets exclude names, phone numbers, emails, exact addresses, GPS coordinates, and free-text personal notes.

## Reproducibility

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Build and train (optional script-first flow):
```bash
python src/build_forecasting_dataset.py
python src/train_two_stage_models.py
```

3. Open and run:
```text
notebooks/lisanegebriel_ethiopia_final_project.ipynb
```

## Optional dashboard

The Streamlit app is a prototype for collecting anonymous outage reports and exploring the dataset. It is not required to reproduce the notebook analysis.

Run:
```bash
streamlit run app/streamlit_app.py
```

## Repository layout

```text
GridSense/
+-- README.md
+-- PROJECT_SUMMARY.md
+-- requirements.txt
+-- .gitignore
+-- notebooks/
¦   +-- lisanegebriel_ethiopia_final_project.ipynb
+-- data/
¦   +-- DATASET.md
¦   +-- collected/
¦   ¦   +-- community_outage_reports.csv
¦   +-- processed/
¦       +-- community_outage_reports_clean.csv
¦       +-- gridsense_forecasting_dataset.csv
¦       +-- local_evidence_dataset.csv
+-- reports/
¦   +-- cards/
¦   +-- tables/
+-- src/
¦   +-- build_forecasting_dataset.py
¦   +-- train_two_stage_models.py
¦   +-- analyze_real_data.py
¦   +-- train_and_evaluate_model.py
+-- app/
    +-- streamlit_app.py
```
