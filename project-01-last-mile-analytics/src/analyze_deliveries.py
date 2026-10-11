from pathlib import Path
import json
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_DIR / "data" / "generated" / "deliveries.csv"
REPORT_DIR = PROJECT_DIR / "reports" / "generated"

def validate_data(df: pd.DataFrame) -> None:
    required = {"order_id", "order_date", "region", "delivery_partner", "distance_km",
        "promised_minutes", "actual_minutes", "status", "delivery_cost", "is_on_time"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if df["order_id"].duplicated().any():
        raise ValueError("order_id must be unique")
    if not set(df["status"].dropna().unique()).issubset({"delivered", "failed"}):
        raise ValueError("Unexpected status value")
    if (df["delivery_cost"] < 0).any() or (df["distance_km"] <= 0).any():
        raise ValueError("Costs must be non-negative and distances positive")
    if (df["status"].eq("failed") & df["actual_minutes"].notna()).any():
        raise ValueError("Failed deliveries must not have actual_minutes")

def summarize(df: pd.DataFrame) -> dict:
    validate_data(df)
    total = len(df)
    delivered = df["status"].eq("delivered")
    failed = df["status"].eq("failed")
    on_time = delivered & df["actual_minutes"].le(df["promised_minutes"])
    delivered_count = int(delivered.sum())
    return {
        "orders": total,
        "delivered_orders": delivered_count,
        "failed_orders": int(failed.sum()),
        "delivery_success_rate": round(delivered_count / total, 4) if total else None,
        "failed_delivery_rate": round(float(failed.sum()) / total, 4) if total else None,
        "on_time_rate_among_delivered": round(float(on_time.sum()) / delivered_count, 4) if delivered_count else None,
        "average_delay_minutes_among_delivered": round(float((df.loc[delivered, "actual_minutes"] - df.loc[delivered, "promised_minutes"]).clip(lower=0).mean()), 2) if delivered_count else None,
        "cost_per_order": round(float(df["delivery_cost"].sum() / total), 2) if total else None,
        "cost_per_successful_delivery": round(float(df["delivery_cost"].sum() / delivered_count), 2) if delivered_count else None,
    }

def grouped_summary(df: pd.DataFrame, column: str) -> pd.DataFrame:
    validate_data(df)
    rows = [{column: value, **summarize(group)} for value, group in df.groupby(column, dropna=False)]
    return pd.DataFrame(rows).sort_values("orders", ascending=False)

if __name__ == "__main__":
    if not DATA_PATH.exists():
        raise SystemExit("Dataset not found. Run src/generate_data.py first.")
    data = pd.read_csv(DATA_PATH)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "overall_metrics.json").write_text(json.dumps(summarize(data), indent=2))
    grouped_summary(data, "region").to_csv(REPORT_DIR / "by_region.csv", index=False)
    grouped_summary(data, "delivery_partner").to_csv(REPORT_DIR / "by_partner.csv", index=False)
    print(json.dumps(summarize(data), indent=2))
    print(f"Reports saved under {REPORT_DIR}")
