"""Generate synthetic risk scores and evaluate operational threshold trade-offs."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score
from threshold_analysis import evaluate_thresholds

PROJECT_DIR = Path(__file__).resolve().parents[1]
REPORT_DIR = PROJECT_DIR / "reports" / "generated"

def generate_scores(n: int = 10000, seed: int = 19):
    if n < 100:
        raise ValueError("n must be at least 100")
    rng = np.random.default_rng(seed)
    y = (rng.random(n) < 0.025).astype(int)  # 2.5% synthetic positive rate
    # Synthetic score distributions only; this is not a trained model.
    p = np.where(y == 1, rng.beta(5, 2, n), rng.beta(1.3, 8, n))
    return y, np.clip(p, 0, 1)

if __name__ == "__main__":
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    y, scores = generate_scores()
    result = evaluate_thresholds(y, scores, thresholds=np.arange(0.1, 1.0, 0.05))
    result["alert_rate"] = result["alerts"] / len(y)
    result["average_precision"] = average_precision_score(y, scores)
    # Hypothetical workload/cost scenario, deliberately explicit and adjustable.
    result["review_cost_units"] = result["alerts"] * 1.0
    result["miss_cost_units"] = result["missed_positives"] * 25.0
    result["total_hypothetical_cost_units"] = result["review_cost_units"] + result["miss_cost_units"]
    result.to_csv(REPORT_DIR / "threshold_tradeoffs.csv", index=False)
    print(result[["threshold", "precision", "recall", "alerts", "missed_positives", "total_hypothetical_cost_units"]].to_string(index=False))
    print(f"Average precision: {average_precision_score(y, scores):.4f}")
    print(f"Report saved under {REPORT_DIR}")
