import numpy as np

def wmape(actual, forecast):
    """Weighted absolute percentage error; undefined when total actual is zero."""
    a, f = np.asarray(actual, dtype=float), np.asarray(forecast, dtype=float)
    if a.shape != f.shape:
        raise ValueError("actual and forecast must have the same shape")
    denominator = np.abs(a).sum()
    return float(np.abs(a - f).sum() / denominator) if denominator else float("nan")

def forecast_bias(actual, forecast):
    """Signed bias: positive values mean overforecasting."""
    a, f = np.asarray(actual, dtype=float), np.asarray(forecast, dtype=float)
    if a.shape != f.shape:
        raise ValueError("actual and forecast must have the same shape")
    denominator = a.sum()
    return float((f - a).sum() / denominator) if denominator else float("nan")
