# Executive summary

## Project
GridSense: A real-data-first analysis of electricity reliability in Addis Ababa.

## Question
To what extent can currently available public evidence and collected community reports explain electricity reliability in Addis Ababa, and support outage-risk prediction?

## Findings
- Addis Ababa has high electricity access, but reliability remains a challenge.
- Official/public evidence reports 882 medium-voltage interruptions and 2,103 interruption hours in a 2019/20 baseline.
- A later public report described more than 25,000 outage-related problems identified in Addis Ababa, with 54% resolved.
- Ethiopia Enterprise Survey indicators show that outages have been a serious business constraint.
- A real community dataset (`n=198`) was collected through a non-personal Streamlit workflow.
- On a held-out test split, trained models outperformed baseline strongly (best: Random Forest, accuracy 0.80, F1-high-risk 0.7619, ROC-AUC 0.9221).

## Engineering decision
The project avoids treating synthetic data as real. It now includes a real-data trained research model and transparent evaluation, while explicitly avoiding operational overclaiming.

