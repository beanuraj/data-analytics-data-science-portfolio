# Project 02 — Retail Demand & Inventory Optimization

## Business question
Can a simple baseline forecast provide a useful benchmark for store-SKU demand, and where is forecast bias likely to create inventory risk?

## Run it
From the repository root:

```bash
python project-02-retail-forecasting/src/forecast_demo.py
```

The pipeline generates two years of synthetic weekly sales for 3 stores and 4 SKUs, holds out the last 13 weeks for each store-SKU pair, and compares two transparent baselines: last-week naive and trailing four-week mean. Outputs are saved under `reports/generated/`.

## Metrics
- **WMAPE** = sum of absolute errors / sum of actual demand. Lower is better.
- **Signed bias** = sum(forecast − actual) / sum(actual). Positive means overforecasting; negative means underforecasting.
- Results are reported per store-SKU pair and summarized across pairs.

## Example run (synthetic data, seed 7)
Across 12 store-SKU groups, mean group-level WMAPE was approximately **16.35%** for the trailing four-week mean versus **22.87%** for the last-week-naive baseline. Mean group-level bias was approximately **−1.71%** and **−0.61%**, respectively. These are illustrative results from generated data; the better baseline depends on the dataset and metric.

## Interpretation
Use the model comparison to identify which baseline is a stronger benchmark, then inspect SKU/store-level errors before making replenishment decisions. Forecast accuracy alone does not determine safety stock: lead times, service targets, capacity, and stockout costs are also required.

## Limitations
This is a reproducible synthetic demonstration, not a production forecast. The simple baselines do not use promotions as predictors, and average group-level WMAPE is not the same as pooled WMAPE. No business savings are claimed.
