# Superstore Corporate Performance Suite

A Streamlit-based interactive dashboard for exploratory data analysis on the Superstore dataset.

## Project Overview

This app reads `superstore.csv`, prepares sales and profit metrics, and renders a multi-tab dashboard with:
- Overview & KPIs
- Sales & Profit Analysis
- Customer Analysis
- Geographic Analysis
- Insights & Recommendations

The dashboard includes filters for year, region, category, and segment, and supports downloading filtered data.

## Installation

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

## Running the App

```bash
streamlit run app.py
```

## Notes

- The app expects `superstore.csv` to be present in the project root.
- Filters are initialized blank, but empty filter selections still apply to all data.
