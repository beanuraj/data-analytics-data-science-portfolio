from pathlib import Path
import numpy as np
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
OUTPUT = PROJECT_DIR / "data" / "generated" / "deliveries.csv"

def generate_deliveries(n: int = 5000, seed: int = 42) -> pd.DataFrame:
    """Generate labelled synthetic delivery data for reproducible practice."""
    if n < 1:
        raise ValueError("n must be at least 1")
    rng = np.random.default_rng(seed)
    regions = np.array(["North", "South", "East", "West"])
    partners = np.array(["Partner_A", "Partner_B", "Partner_C"])
    dates = pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 180, size=n), unit="D")
    distance = np.round(rng.gamma(shape=2.2, scale=3.0, size=n) + 0.5, 2)
    promised = np.clip((25 + distance * 4 + rng.normal(0, 5, n)).round(), 20, 120).astype(int)
    region = rng.choice(regions, n, p=[0.27, 0.28, 0.20, 0.25])
    partner = rng.choice(partners, n, p=[0.40, 0.35, 0.25])
    # Illustrative synthetic relationships only; not real-world estimates.
    partner_delay = pd.Series(partner).map({"Partner_A": 1, "Partner_B": 4, "Partner_C": 7}).to_numpy()
    actual = np.maximum(10, (promised + rng.normal(0, 10, n) + partner_delay).round()).astype(float)
    fail_prob = np.clip(0.035 + distance * 0.002 + (partner == "Partner_C") * 0.025, 0.02, 0.18)
    failed = rng.random(n) < fail_prob
    actual[failed] = np.nan
    status = np.where(failed, "failed", "delivered")
    cost = np.round(18 + distance * 3.2 + rng.gamma(2.0, 4.0, n), 2)
    out = pd.DataFrame({
        "order_id": [f"ORD-{i:06d}" for i in range(1, n + 1)],
        "order_date": pd.to_datetime(dates).date.astype(str),
        "region": region, "delivery_partner": partner, "distance_km": distance,
        "promised_minutes": promised, "actual_minutes": actual, "status": status,
        "delivery_cost": cost,
    })
    out["is_on_time"] = np.where(out["status"].eq("delivered"),
        out["actual_minutes"].le(out["promised_minutes"]), np.nan)
    return out

if __name__ == "__main__":
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df = generate_deliveries()
    df.to_csv(OUTPUT, index=False)
    print(f"Wrote {len(df):,} synthetic rows to {OUTPUT}")
