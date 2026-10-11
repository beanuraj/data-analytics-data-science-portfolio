import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from threshold_analysis import evaluate_thresholds

def test_threshold_metrics():
    result = evaluate_thresholds([0, 1, 1, 0], [0.1, 0.9, 0.4, 0.2], [0.5])
    assert result.loc[0, "alerts"] == 1
    assert result.loc[0, "recall"] == pytest.approx(0.5)

def test_invalid_probabilities_rejected():
    with pytest.raises(ValueError):
        evaluate_thresholds([0, 1], [0.2, 1.2])
