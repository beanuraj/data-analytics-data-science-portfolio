# Synthetic data dictionary

One row represents one delivery order. All records are synthetic.

| Column | Type | Description |
|---|---|---|
| order_id | string | Synthetic unique identifier |
| order_date | date | Synthetic order date |
| region | string | Synthetic operating region |
| delivery_partner | string | Synthetic partner |
| distance_km | float | Estimated delivery distance |
| promised_minutes | integer | Promised duration |
| actual_minutes | float/null | Actual duration; null for failures |
| status | string | delivered or failed |
| delivery_cost | float | Synthetic order cost |
| is_on_time | boolean/null | Whether a delivered order met its promise |

The data generator uses simplified illustrative relationships. It is not calibrated to real logistics operations.
