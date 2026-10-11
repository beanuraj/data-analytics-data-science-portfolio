import sys
from pathlib import Path
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from analyze_deliveries import summarize, validate_data
from generate_data import generate_deliveries

def test_generator_is_reproducible():
    pd.testing.assert_frame_equal(generate_deliveries(20, 7), generate_deliveries(20, 7))

def test_summary_metrics():
    df = pd.DataFrame({
        "order_id": ["a", "b", "c"], "order_date": ["2025-01-01"] * 3,
        "region": ["North"] * 3, "delivery_partner": ["A"] * 3,
        "distance_km": [1.0, 2.0, 3.0], "promised_minutes": [30, 30, 30],
        "actual_minutes": [25.0, 40.0, float("nan")],
        "status": ["delivered", "delivered", "failed"], "delivery_cost": [20.0, 30.0, 25.0],
        "is_on_time": [True, False, float("nan")]})
    result = summarize(df)
    assert result["orders"] == 3
    assert result["delivery_success_rate"] == pytest.approx(2 / 3, abs=1e-4)
    assert result["failed_delivery_rate"] == pytest.approx(1 / 3, abs=1e-4)
    assert result["on_time_rate_among_delivered"] == pytest.approx(1 / 2, abs=1e-4)
    assert result["cost_per_order"] == pytest.approx(25.0)
    assert result["cost_per_successful_delivery"] == pytest.approx(37.5)

def test_duplicate_order_ids_rejected():
    df = generate_deliveries(5)
    df.loc[1, "order_id"] = df.loc[0, "order_id"]
    with pytest.raises(ValueError, match="unique"):
        validate_data(df)
