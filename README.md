# GridSense

**Learning electricity outage patterns from local public evidence and building a responsible path toward future outage-risk prediction.**

This is a Kujenga final project by Lisan A. The project is local to Addis Ababa and focuses on electricity reliability: a problem that affects students, households, small businesses, and daily planning.

## Why this project matters

Addis Ababa has high electricity access, but reliability, quality, and availability remain challenges. GridSense asks what can be learned from public evidence today, and what data would be required to build a responsible prediction model tomorrow.

## Important data choice

The organisers advised avoiding synthetic datasets if possible. This version therefore avoids using synthetic data as the main dataset. The repository contains public, non-personal evidence files and a safe future report template.
It also includes real collected community outage reports used for model training and evaluation.

## Repository structure

```text
app/                       Optional Streamlit dashboard
notebooks/                 Final Jupyter notebook
src/                       Small reproducible analysis and formula scripts
data/raw/                  Public, non-personal data files
data/collected/            Real community reports collected via Streamlit form
data/processed/            Combined local evidence dataset
reports/figures/           SVG visualizations
reports/cards/             Data card and model card
```

## Main notebook

`notebooks/lisanegebriel_ethiopia_final_project.ipynb`

## Reproducibility checklist

- Python version: `Python 3.10+` (tested with 3.10/3.11)
- Create environment (recommended): `python -m venv .venv` then activate it
- Install dependencies: `pip install -r requirements.txt`
- Run order:
  1. `python src/analyze_real_data.py`
  2. `python src/regression_formula_demo.py`
  3. `python src/train_and_evaluate_model.py`
  4. Open and run all cells in `notebooks/lisanegebriel_ethiopia_final_project.ipynb`
- Expected outputs after step 1:
  - `reports/tables/derived_kpis.json`
  - `reports/tables/outage_severity_index_components.csv`
  - figures in `reports/figures/` used by the notebook
- Expected outputs after step 3:
  - `reports/tables/model_metrics.json` with baseline vs trained model metrics
- Expected outputs in the notebook:
  - reliability context figures render
  - severity index component table prints
  - one-sample proportion test output (z-statistic, one-sided p-value, 95% CI)

## How to run quickly

```bash
python src/analyze_real_data.py
python src/regression_formula_demo.py
```

Optional dashboard:

```bash
streamlit run app/streamlit_app.py
```

The Streamlit app includes a privacy-safe form that appends real reports to:

`data/collected/community_outage_reports.csv`

## What this project does not claim

It does not claim to operate an official outage prediction system. The current real event-level dataset is sufficient for research training/evaluation, but still limited for production deployment.

## Current model status

- Trained on real collected data: `data/collected/community_outage_reports.csv` (`n=198`).
- Evaluation script: `src/train_and_evaluate_model.py`.
- Metrics output: `reports/tables/model_metrics.json`.
- Best current model (by F1-high-risk): Random Forest.

