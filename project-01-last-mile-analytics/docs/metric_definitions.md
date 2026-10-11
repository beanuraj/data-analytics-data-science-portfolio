# Metric definitions

All rates use this project's generated dataset. Show denominators and state which statuses are included.

- **Delivery success rate** = delivered orders / all orders.
- **Failed delivery rate** = failed orders / all orders.
- **On-time rate among delivered orders** = delivered orders delivered at or before the promised duration / delivered orders.
- **Average delay minutes** = mean of max(actual duration - promised duration, 0) among delivered orders.
- **Cost per order** = total delivery cost / all orders.
- **Cost per successful delivery** = total delivery cost / delivered orders.

These are portfolio definitions, not universal industry standards. In real operations, confirm cancellation treatment, timezone rules, redelivery costs, and official KPI definitions.
