# Data Analytics & Data Science Portfolio

Advanced, business-focused projects using public or synthetic data. The portfolio demonstrates KPI design, SQL, Python, forecasting, machine-learning evaluation, testing, and decision-oriented communication.

## Projects
- **01 — Last-Mile Delivery Intelligence:** delivery service levels, failures, cost, and operational drivers.
- **02 — Retail Demand & Inventory Optimization:** forecast accuracy, bias, and inventory risk.
- **03 — Financial Crime & Alert Optimization:** model thresholds, false-positive workload, and missed-case trade-offs.

## Principles
- No confidential employer data, code, dashboards, documents, or internal metrics.
- Synthetic data is explicitly labelled and never presented as real-world evidence.
- Public datasets will be used only after checking terms and documenting their source.
- Metrics and model results will be generated and tested before being quoted in a CV.
- Third-party code and data will be attributed according to their licenses.

## Quick start
Python 3.10+ recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
python project-01-last-mile-analytics/src/generate_data.py
python project-01-last-mile-analytics/src/analyze_deliveries.py
```

See each project README for scope, assumptions, and commands. This is an initial scaffold; run it locally and verify results before publication.
