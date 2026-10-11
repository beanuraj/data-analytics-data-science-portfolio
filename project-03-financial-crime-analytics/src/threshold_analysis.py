import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

def evaluate_thresholds(y_true, probabilities, thresholds=None):
    """Evaluate classification metrics across probability thresholds."""
    y, p = np.asarray(y_true), np.asarray(probabilities, dtype=float)
    if y.shape != p.shape:
        raise ValueError("y_true and probabilities must have the same shape")
    if not np.isin(y, [0, 1]).all():
        raise ValueError("y_true must contain only 0 and 1")
    if not np.isfinite(p).all() or ((p < 0) | (p > 1)).any():
        raise ValueError("probabilities must be finite values in [0, 1]")
    if thresholds is None:
        thresholds = np.arange(0.1, 1.0, 0.1)
    rows = []
    for threshold in thresholds:
        predicted = (p >= threshold).astype(int)
        rows.append({
            "threshold": float(threshold),
            "precision": float(precision_score(y, predicted, zero_division=0)),
            "recall": float(recall_score(y, predicted, zero_division=0)),
            "f1": float(f1_score(y, predicted, zero_division=0)),
            "alerts": int(predicted.sum()),
            "missed_positives": int(((y == 1) & (predicted == 0)).sum()),
        })
    return pd.DataFrame(rows)
