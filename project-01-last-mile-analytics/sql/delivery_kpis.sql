-- Assumes a deliveries table matching docs/data_dictionary.md.
-- Amazon Redshift-compatible SQL.

SELECT
    COUNT(*) AS total_orders,
    SUM(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) AS delivered_orders,
    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) AS failed_orders,
    1.0 * SUM(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0) AS delivery_success_rate,
    1.0 * SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0) AS failed_delivery_rate,
    1.0 * SUM(CASE WHEN status = 'delivered' AND actual_minutes <= promised_minutes THEN 1 ELSE 0 END)
        / NULLIF(SUM(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END), 0)
        AS on_time_rate_among_delivered,
    AVG(CASE WHEN status = 'delivered'
        THEN GREATEST(actual_minutes - promised_minutes, 0) END) AS average_delay_minutes,
    SUM(delivery_cost) / NULLIF(COUNT(*), 0) AS cost_per_order,
    SUM(delivery_cost) / NULLIF(SUM(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END), 0)
        AS cost_per_successful_delivery
FROM deliveries;

-- Descriptive comparisons do not establish causality.
SELECT delivery_partner, COUNT(*) AS orders,
    AVG(CASE WHEN status = 'delivered' AND actual_minutes <= promised_minutes THEN 1.0 ELSE 0.0 END)
        AS on_time_rate_all_orders,
    AVG(CASE WHEN status = 'failed' THEN 1.0 ELSE 0.0 END) AS failure_rate,
    AVG(delivery_cost) AS avg_cost_per_order
FROM deliveries
GROUP BY delivery_partner
ORDER BY orders DESC;
