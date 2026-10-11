# Project 01 — Last-Mile Delivery Intelligence

## Business question
Which regions, delivery partners, and operating conditions are associated with late or failed deliveries and higher cost per successful delivery?

## Scope
This implementation creates a reproducible **synthetic** delivery dataset and calculates operational KPIs. It is not real company data and does not claim real-world savings.

## Metrics
- Delivery success rate = delivered orders / all orders.
- Failed delivery rate = failed orders / all orders.
- On-time rate among delivered orders.
- Average delay minutes among delivered orders.
- Cost per order and cost per successful delivery.

Definitions and assumptions are in `docs/metric_definitions.md`. SQL equivalents are in `sql/delivery_kpis.sql`.

## Run from the repository root
```bash
pip install -r requirements.txt
python project-01-last-mile-analytics/src/generate_data.py
python project-01-last-mile-analytics/src/analyze_deliveries.py
pytest
```

Generated data and reports are ignored by Git by default.

## Planned enhancements
1. Add deeper data-quality and schema checks.
2. Analyze performance by weekday, region, partner, and order volume.
3. Test whether segment differences are statistically meaningful.
4. Build a dashboard with metric glossary and drill-through.
5. Add cost scenarios with explicit assumptions.
6. Consider a public real-world dataset after checking its license and suitability.

## Attribution
This scaffold is newly authored for this portfolio. No employer code or internal data is included. Public datasets or third-party components added later must be documented with their sources and licenses.
