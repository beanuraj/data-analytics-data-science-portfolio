"""Synthetic retail demand demo comparing simple weekly forecasting baselines."""
from pathlib import Path
import numpy as np
import pandas as pd
from metrics import wmape, forecast_bias

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data" / "generated"
REPORT_DIR = PROJECT_DIR / "reports" / "generated"

def generate_sales(seed: int = 7, weeks: int = 104) -> pd.DataFrame:
    if weeks < 20:
        raise ValueError("weeks must be at least 20")
    rng = np.random.default_rng(seed)
    rows = []
    start = pd.Timestamp("2024-01-01")
    for store in ["Store_A", "Store_B", "Store_C"]:
        for sku in ["SKU_001", "SKU_002", "SKU_003", "SKU_004"]:
            base = rng.integers(25, 100)
            trend = rng.uniform(-0.08, 0.16)
            for w in range(weeks):
                seasonal = 1 + 0.18 * np.sin(2 * np.pi * w / 52)
                promo = int(rng.random() < 0.12)
                demand = max(0, round(base * seasonal * (1 + trend * w / 52) * (1.45 if promo else 1) + rng.normal(0, base * 0.12)))
                rows.append((start + pd.Timedelta(weeks=w), store, sku, promo, demand))
    return pd.DataFrame(rows, columns=["week_start", "store", "sku", "promo", "units_sold"])

def evaluate(data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (store, sku), group in data.sort_values("week_start").groupby(["store", "sku"]):
        group = group.reset_index(drop=True)
        # Hold out the final 13 weeks; no future values enter either baseline.
        split = len(group) - 13
        train, test = group.iloc[:split].copy(), group.iloc[split:].copy()
        last_week = train["units_sold"].iloc[-1]
        recent_mean = train["units_sold"].tail(4).mean()
        for model, forecast in [("last_week_naive", np.repeat(last_week, len(test))),
                                ("four_week_mean", np.repeat(recent_mean, len(test)))]:
            rows.append({"store": store, "sku": sku, "model": model,
                         "test_weeks": len(test), "wmape": wmape(test.units_sold, forecast),
                         "bias": forecast_bias(test.units_sold, forecast),
                         "actual_units": int(test.units_sold.sum()),
                         "forecast_units": round(float(np.sum(forecast)), 2)})
    return pd.DataFrame(rows)

if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True); REPORT_DIR.mkdir(parents=True, exist_ok=True)
    df = generate_sales(); df.to_csv(DATA_DIR / "weekly_sales.csv", index=False)
    result = evaluate(df); result.to_csv(REPORT_DIR / "baseline_comparison.csv", index=False)
    overall = result.groupby("model").apply(lambda x: pd.Series({
        "mean_sku_store_wmape": x.wmape.mean(), "mean_sku_store_bias": x.bias.mean(),
        "sku_store_groups": len(x)}), include_groups=False).reset_index()
    overall.to_csv(REPORT_DIR / "model_summary.csv", index=False)
    print(overall.to_string(index=False))
    print(f"Reports saved under {REPORT_DIR}")
