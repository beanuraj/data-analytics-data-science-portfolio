# Data Analytics & Data Science Portfolio

Business-focused portfolio demonstrating SQL, Python, KPI design, forecasting evaluation, and decision-oriented analytics using synthetic datasets. No employer data, proprietary code, or confidential business results are included.

## Projects

| Project | Business problem | Skills demonstrated |
|---|---|---|
| [01 — Last-Mile Delivery Intelligence](project-01-last-mile-analytics/README.md) | Delivery reliability, delay severity, and cost by region/partner | Python, pandas, SQL, data validation, visual reporting, business recommendations |
| [02 — Retail Demand & Inventory Optimization](project-02-retail-forecasting/README.md) | Compare demand forecasting baselines and measure bias | Python, time-aware validation, WMAPE, forecast bias |
| [03 — Financial Crime Alert Optimization](project-03-financial-crime-analytics/README.md) | Quantify alert threshold, workload, and missed-positive trade-offs | Python, classification metrics, threshold/cost analysis |

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python project-01-last-mile-analytics/src/generate_data.py
python project-01-last-mile-analytics/src/analyze_deliveries.py
python project-02-retail-forecasting/src/forecast_demo.py
python project-03-financial-crime-analytics/src/threshold_demo.py
pytest -q
```

Each project documents assumptions, metric definitions, and limitations. Synthetic outputs are illustrative and do not represent any employer's actual performance.

## About
Data analytics and data science practitioner focused on translating business questions into measurable KPIs, robust analysis, and actionable recommendations.
