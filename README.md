# Superstore Corporate Performance Suite

An interactive Streamlit dashboard for analyzing the Superstore sales dataset.

## Project Summary

This repository contains:
- `app.py` — the Streamlit dashboard application
- `superstore.csv` — the data source used for sales, profit, and customer analysis
- `README.md` — setup and usage instructions

The dashboard provides a multi-tab user interface with:
- Overview & KPIs
- Sales & Profit Analysis
- Customer Analysis
- Geographic Analysis
- Insights & Recommendations

## Features

- Filter data by year, region, category, and segment
- Automatically treat empty filter selections as full-data selection
- Display executive-level KPIs and visual analysis charts
- Download filtered results as CSV

## Setup

1. Create a Python virtual environment:

```bash
python -m venv .venv
```

2. Activate the environment:

- Windows PowerShell:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- Windows Command Prompt:
  ```cmd
  .\.venv\Scripts\activate.bat
  ```

3. Install dependencies:

```bash
pip install streamlit pandas plotly
```

## Run the Dashboard

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal.

## Data

`superstore.csv` is included in the project root so the app can run immediately after dependency installation.

## Notes

- If filters are cleared, the dashboard still works over the full dataset.
- Ensure the CSV file remains in the same folder as `app.py`.
