# Data Quality Checker
# live_project:https://data-quality-checkerx.streamlit.app/
A lightweight toolkit to analyze dataset quality and produce an overall data-quality score and dashboard.

## Features
- Basic health checks (shape, missing values, duplicates, dtypes)
- Distribution analysis (skewness, outliers, zero-variance)
- Feature analysis (constant cols, high-cardinality, correlation)
- Target analysis (class imbalance or regression target stats, feature-target correlation)
- Streamlit dashboard with visual reports

## Prerequisites
- Python 3.8+
- Install dependencies:

```bash
pip install -r requirements.txt
```

## Quick checks
- Run the Phase 4 unit test (classification example):

```bash
python Data_checks/checks/class_imalance.py
```

## Run the dashboard
- Start the interactive Streamlit dashboard:

```bash
streamlit run Data_checks/dashboard.py
```

Open the URL printed by Streamlit (usually http://localhost:8501).

## Project layout
- `Data_checks/` — main package
- `Data_checks/checks/` — analysis phases (Phase1..Phase5)
- `requirements.txt` — Python dependencies

## Next steps
- Run the dashboard and upload a CSV to see the report.

If you want, I can run the dashboard now and verify end-to-end.
