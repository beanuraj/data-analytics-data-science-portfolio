"""Create decision-oriented delivery KPI reports from synthetic data."""
from pathlib import Path
import json
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_DIR / "data" / "generated" / "deliveries.csv"
REPORT_DIR = PROJECT_DIR / "reports" / "generated"
DASHBOARD_DIR = PROJECT_DIR / "dashboards"


def validate_data(df: pd.DataFrame) -> None:
    required = {"order_id", "order_date", "region", "delivery_partner", "distance_km",
        "promised_minutes", "actual_minutes", "status", "delivery_cost", "is_on_time"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if df.empty:
        raise ValueError("Dataset must contain at least one row")
    if df["order_id"].isna().any() or df["order_id"].duplicated().any():
        raise ValueError("order_id must be populated and unique")
    if df[list(required - {"actual_minutes", "is_on_time"})].isna().any().any():
        raise ValueError("Required non-outcome fields must not contain nulls")
    if not set(df["status"].dropna().unique()).issubset({"delivered", "failed"}):
        raise ValueError("Unexpected status value")
    if (df["delivery_cost"] < 0).any() or (df["distance_km"] <= 0).any():
        raise ValueError("Costs must be non-negative and distances positive")
    if (df["promised_minutes"] <= 0).any():
        raise ValueError("Promised time must be positive")
    if (df["status"].eq("failed") & df["actual_minutes"].notna()).any():
        raise ValueError("Failed deliveries must not have actual_minutes")
    if (df["status"].eq("delivered") & df["actual_minutes"].isna()).any():
        raise ValueError("Delivered orders must have actual_minutes")


def summarize(df: pd.DataFrame) -> dict:
    validate_data(df)
    total = len(df)
    delivered = df["status"].eq("delivered")
    failed = df["status"].eq("failed")
    on_time = delivered & df["actual_minutes"].le(df["promised_minutes"])
    delivered_count = int(delivered.sum())
    delay = (df.loc[delivered, "actual_minutes"] - df.loc[delivered, "promised_minutes"]).clip(lower=0)
    return {
        "orders": total,
        "delivered_orders": delivered_count,
        "failed_orders": int(failed.sum()),
        "delivery_success_rate": round(delivered_count / total, 4),
        "failed_delivery_rate": round(float(failed.sum()) / total, 4),
        "on_time_rate_among_delivered": round(float(on_time.sum()) / delivered_count, 4) if delivered_count else None,
        "average_delay_minutes_among_delivered": round(float(delay.mean()), 2) if delivered_count else None,
        "p90_delay_minutes_among_delivered": round(float(delay.quantile(0.90)), 2) if delivered_count else None,
        "cost_per_order": round(float(df["delivery_cost"].sum() / total), 2),
        "cost_per_successful_delivery": round(float(df["delivery_cost"].sum() / delivered_count), 2) if delivered_count else None,
        "total_delivery_cost": round(float(df["delivery_cost"].sum()), 2),
    }


def grouped_summary(df: pd.DataFrame, column: str) -> pd.DataFrame:
    validate_data(df)
    rows = [{column: value, **summarize(group)} for value, group in df.groupby(column, dropna=False)]
    return pd.DataFrame(rows).sort_values("orders", ascending=False).reset_index(drop=True)


def build_recommendations(overall: dict, regions: pd.DataFrame, partners: pd.DataFrame) -> list[dict]:
    """Create transparent rules-based recommendations, not causal claims."""
    recs = []
    worst_region = regions.sort_values(["failed_delivery_rate", "orders"], ascending=[False, False]).iloc[0]
    worst_partner = partners.sort_values(["failed_delivery_rate", "average_delay_minutes_among_delivered"], ascending=False).iloc[0]
    recs.append({
        "priority": 1, "area": "Delivery failures", "finding":
        f"{worst_region['region']} has the highest observed failure rate ({worst_region['failed_delivery_rate']:.1%}) across {int(worst_region['orders']):,} orders.",
        "recommended_action": "Review failed-order reasons and operational conditions in this region; compare like-for-like distance and order-volume segments.",
        "success_metric": "Failed delivery rate", "caveat": "Descriptive signal only; validate sample size and mix before changing operations."
    })
    recs.append({
        "priority": 2, "area": "Partner performance", "finding":
        f"{worst_partner['delivery_partner']} has the highest observed failure rate ({worst_partner['failed_delivery_rate']:.1%}) among partners.",
        "recommended_action": "Audit handoff, capacity, and exception processes with the partner; compare performance after controlling for distance and region.",
        "success_metric": "Failure rate and on-time rate", "caveat": "Partner-level differences may reflect different delivery mixes and do not prove causation."
    })
    recs.append({
        "priority": 3, "area": "Customer promise", "finding":
        f"The overall on-time rate among delivered orders is {overall['on_time_rate_among_delivered']:.1%}; the 90th percentile of positive delay is {overall['p90_delay_minutes_among_delivered']:.1f} minutes.",
        "recommended_action": "Inspect high-delay routes and time windows, then test revised promise buffers only for consistently high-variance segments.",
        "success_metric": "On-time rate and 90th-percentile delay", "caveat": "Test changes with a defined comparison period and monitor cost and cancellations as guardrails."
    })
    return recs


def create_charts(regions: pd.DataFrame, partners: pd.DataFrame) -> list[str]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)
    generated = []
    for frame, dimension, filename, title in [
        (regions, "region", "on_time_by_region.png", "On-time rate by region"),
        (partners, "delivery_partner", "failure_rate_by_partner.png", "Failure rate by delivery partner"),
    ]:
        metric = "on_time_rate_among_delivered" if dimension == "region" else "failed_delivery_rate"
        ordered = frame.sort_values(metric, ascending=(dimension == "delivery_partner"))
        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.bar(ordered[dimension].astype(str), ordered[metric] * 100)
        ax.set_title(title)
        ax.set_ylabel("Percent")
        ax.set_ylim(0, max(100, float((ordered[metric] * 100).max() * 1.15)))
        ax.grid(axis="y", alpha=0.25)
        ax.spines[["top", "right"]].set_visible(False)
        fig.tight_layout()
        path = DASHBOARD_DIR / filename
        fig.savefig(path, dpi=160, bbox_inches="tight")
        plt.close(fig)
        generated.append(str(path.relative_to(PROJECT_DIR)))
    return generated


if __name__ == "__main__":
    if not DATA_PATH.exists():
        raise SystemExit("Dataset not found. Run src/generate_data.py first.")
    data = pd.read_csv(DATA_PATH)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    overall = summarize(data)
    regions = grouped_summary(data, "region")
    partners = grouped_summary(data, "delivery_partner")
    (REPORT_DIR / "overall_metrics.json").write_text(json.dumps(overall, indent=2))
    regions.to_csv(REPORT_DIR / "by_region.csv", index=False)
    partners.to_csv(REPORT_DIR / "by_partner.csv", index=False)
    regions.sort_values(["failed_delivery_rate", "orders"], ascending=[False, False]).to_csv(
        REPORT_DIR / "region_risk_prioritization.csv", index=False)
    partners.sort_values(["failed_delivery_rate", "average_delay_minutes_among_delivered"], ascending=False).to_csv(
        REPORT_DIR / "partner_risk_prioritization.csv", index=False)
    recommendations = build_recommendations(overall, regions, partners)
    (REPORT_DIR / "recommendations.json").write_text(json.dumps(recommendations, indent=2))
    chart_paths = create_charts(regions, partners)
    print(json.dumps(overall, indent=2))
    print("\nPriority recommendations:")
    for rec in recommendations:
        print(f"{rec['priority']}. {rec['area']}: {rec['finding']} Action: {rec['recommended_action']}")
    print(f"\nReports saved under {REPORT_DIR}")
    print(f"Charts saved: {', '.join(chart_paths)}")
