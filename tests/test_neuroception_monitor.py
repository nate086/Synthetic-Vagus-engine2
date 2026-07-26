import pytest
from neuroception_monitor import NeuroceptionMonitor


def test_basic_range():
    m = NeuroceptionMonitor()
    assert 0.0 <= m.evaluate({}) <= 1.0


def test_low_vs_high():
    m = NeuroceptionMonitor()
    low = m.evaluate({"heart_rate_variability": 1.0, "skin_conductance": 0.0})
    high = m.evaluate({"heart_rate_variability": 0.0, "skin_conductance": 1.0})
    assert low < high
