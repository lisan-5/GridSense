# GridSense

GridSense is a Kujenga final project that studies electricity outage patterns in Addis Ababa using 198 anonymous community-reported outage records.

The project investigates:
1. When outages are most commonly reported.
2. Which sub-cities report higher outage burden.
3. Whether rainy/stormy conditions are associated with longer duration.
4. Whether time, weather, and location features can support a responsible high-risk outage model.

## Main notebook

`notebooks/lisanegebriel_ethiopia_final_project.ipynb`

## Dataset

The main dataset is `data/processed/community_outage_reports_clean.csv`.

It contains anonymous community outage reports collected from Addis Ababa residents. The public dataset does not include names, phone numbers, emails, exact addresses, GPS coordinates, or free-text comments.

## Reproducibility

1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Open and run:
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
├── README.md
├── PROJECT_SUMMARY.md
├── requirements.txt
├── .gitignore
├── notebooks/
│   └── lisanegebriel_ethiopia_final_project.ipynb
├── data/
│   ├── DATASET.md
│   ├── collected/
│   │   └── community_outage_reports.csv
│   └── processed/
│       ├── community_outage_reports_clean.csv
│       └── local_evidence_dataset.csv
├── reports/
│   ├── figures/
│   └── cards/
├── src/
│   ├── analyze_real_data.py
│   └── train_and_evaluate_model.py
└── app/
    └── streamlit_app.py
```
