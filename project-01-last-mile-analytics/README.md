# Project 01 — Last-Mile Delivery Intelligence

## Business problem
A delivery operation needs to improve reliability without losing sight of cost. This project measures delivery success, on-time performance, delay severity, and delivery cost by region and partner.

## Run it
From the repository root:

```bash
pip install -r requirements.txt
python project-01-last-mile-analytics/src/generate_data.py
python project-01-last-mile-analytics/src/analyze_deliveries.py
```

The generator creates 5,000 deterministic synthetic orders. Reports are written to `reports/generated/`: overall KPIs, region comparison, partner comparison, and a prioritized diagnostic summary. SQL equivalents are in `sql/delivery_kpis.sql`.

## Questions answered
- What share of orders are successfully delivered and on time?
- Which regions and delivery partners have the highest delay and failure risk?
- What is the cost per order and per successful delivery?
- Which segments should operations investigate first?

## Method and caveats
- A failed delivery is not counted as on-time; on-time rate uses delivered orders as its denominator.
- Cost per successful delivery uses total delivery cost divided by successful deliveries, so failed-order costs remain visible.
- Data is synthetic and designed to demonstrate workflow and analysis, not to represent actual company performance. Segment differences are descriptive, not causal.

## Deliverables
- Reproducible synthetic data generation
- Data validation and KPI calculations
- Segment-level CSV outputs and JSON summary
- SQL KPI query and metric definitions
- Unit tests
