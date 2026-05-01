# GridSense

**GridSense** is a Kujenga final project that studies electricity outage patterns in Addis Ababa using anonymous community reports. The project focuses on a local problem: electricity interruptions affect students, households, small businesses, internet access, productivity, and daily planning.

GridSense turns community outage reports into a structured **community-report window dataset** and uses a two-stage modelling approach to produce practical local insights.

## Project goal

The goal of this project is to answer:

> Can anonymous community outage reports be used to understand electricity outage patterns in Addis Ababa and build a responsible early risk signal for local planning?

GridSense does **not** claim to observe official electricity utility outage truth. Instead, it estimates the probability that an outage will be captured in community reports for a given sub-city and time window. This makes it a **community-based early attention signal**, not an official utility forecasting system.

## Main research questions

1. When are electricity outages most commonly reported in Addis Ababa?
2. Which sub-cities and time windows show stronger reported-outage signals?
3. Are rainy or stormy conditions associated with longer reported outage duration?
4. Can community reports be transformed into a useful time-window dataset for local outage-risk analysis?
5. If an outage is reported, can we estimate likely severity or duration?

## Methodology

The project uses a two-stage modelling system.

### Stage 1: Community outage-report risk model

Stage 1 estimates the probability that an outage report will be captured for a given sub-city and time window.

This model uses safe, pre-report features such as:

- sub-city
- day of week
- hour block / time window

The output is interpreted as a **community-reported outage risk signal**, not official outage occurrence.

### Stage 2: Conditional impact model

Stage 2 is applied when an outage has been reported. It estimates likely outage impact using severity and duration models.

This stage helps answer:

- Is the reported outage likely to be high severity?
- How long might the outage last?
- Which reports should receive more attention?

## Dataset

The project uses anonymous community-reported outage data collected from Addis Ababa residents.

### Main datasets

- `data/collected/community_outage_reports.csv`  
  Raw anonymous intake data.

- `data/processed/community_outage_reports_clean.csv`  
  Clean event-level community outage reports.

- `data/processed/gridsense_forecasting_dataset.csv`  
  Community-report window dataset used for Stage 1 modelling.

- `data/processed/local_evidence_dataset.csv`  
  Supporting local evidence dataset.

### Current dataset scale

The notebook uses:

- 198 community outage events
- 1,584 sub-city / time-window records
- 11 Addis Ababa sub-cities
- 18 dates
- 8 three-hour windows per day

### Privacy

All public datasets exclude:

- names
- phone numbers
- emails
- exact home addresses
- GPS coordinates
- free-text personal notes
- any direct personal identifiers

The project is designed to be privacy-aware and safe to share in a public GitHub repository.

## Kujenga course connection

This project follows the Kujenga final project spirit: choose a meaningful local problem, collect or organize data, clean it, analyze it, visualize it, apply mathematical or AI methods, and explain the results clearly.

GridSense uses several Kujenga concepts:

| Kujenga concept | How it appears in GridSense |
|---|---|
| Local real-world problem | Electricity reliability in Addis Ababa |
| Data cleaning | Cleaning anonymous community reports |
| Visualization | Outage patterns by time, sub-city, weather, and severity |
| Hypothesis testing | Comparing rainy/stormy and non-rainy outage duration |
| Regression | Modelling reported outage duration |
| Mathematical modelling | Turning event reports into time-window records |
| Machine learning | Two-stage risk and impact modelling |
| Responsible interpretation | Distinguishing community-report signal from official outage truth |

## Main notebook

The main notebook is:

```text
notebooks/lisanegebriel_ethiopia_final_project.ipynb
```

The notebook includes:

- local problem framing
- dataset description
- privacy and ethics notes
- data cleaning
- exploratory data analysis
- visualizations
- t-test
- regression
- two-stage machine learning system
- model evaluation
- practical interpretation
- limitations
- final conclusion

## Repository layout

```text
GridSense/
|-- README.md
|-- PROJECT_SUMMARY.md
|-- requirements.txt
|-- .gitignore
|
|-- notebooks/
|   |-- lisanegebriel_ethiopia_final_project.ipynb
|
|-- data/
|   |-- DATASET.md
|   |
|   |-- collected/
|   |   |-- community_outage_reports.csv
|   |
|   |-- processed/
|       |-- community_outage_reports_clean.csv
|       |-- gridsense_forecasting_dataset.csv
|       |-- local_evidence_dataset.csv
|
|-- reports/
|   |-- cards/
|   |-- tables/
|
|-- src/
|   |-- build_forecasting_dataset.py
|   |-- train_two_stage_models.py
|   |-- analyze_real_data.py
|   |-- train_and_evaluate_model.py
|
|-- app/
    |-- streamlit_app.py
```

## Reproducibility

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Optional script-first workflow

To rebuild the processed dataset and train the models from scripts:

```bash
python src/build_forecasting_dataset.py
python src/train_two_stage_models.py
```

### 3. Run the notebook

Open and run:

```text
notebooks/lisanegebriel_ethiopia_final_project.ipynb
```

For final submission, the notebook should be run from top to bottom and saved with outputs visible.

## Optional Streamlit dashboard

The Streamlit app is an optional prototype for collecting anonymous outage reports and exploring the dataset. It is not required to reproduce the notebook analysis.

Run:

```bash
streamlit run app/streamlit_app.py
```

## Interpretation

GridSense should be interpreted as a **community-based outage report intelligence tool**.

It can help identify:

- time windows with stronger reported-outage signals
- sub-cities with higher report activity
- reported outages that may have higher severity
- patterns that can support better local planning

It should not be interpreted as an official electricity utility forecasting system.

## Practical value

GridSense can support:

- students planning study and charging time
- households preparing for disruption
- small businesses planning backup energy use
- local organizers identifying where reporting coverage is weak
- future researchers building stronger electricity reliability datasets for Addis Ababa

## Future improvements

A stronger future version of GridSense could include:

1. More community reports collected over a longer period.
2. Confirmed no-outage check-ins.
3. Official planned interruption notices.
4. Real weather data for every time window.
5. More precise location grouping while preserving privacy.
6. A public dashboard for local outage awareness.

## Author

**Lisanegebriel Abay**
Ethiopia
Kujenga Final Project
