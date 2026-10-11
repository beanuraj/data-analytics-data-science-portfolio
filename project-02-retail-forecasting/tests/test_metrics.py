import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from metrics import wmape, forecast_bias

def test_wmape():
    assert wmape([100, 200], [90, 220]) == pytest.approx(30 / 300)

def test_positive_bias_means_overforecast():
    assert forecast_bias([100, 100], [110, 120]) == pytest.approx(0.15)

def test_zero_denominator_is_nan():
    assert wmape([0, 0], [1, 2]) != wmape([0, 0], [1, 2])
