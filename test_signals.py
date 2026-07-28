"""Tests for synthetic signal generation."""

import numpy as np
from sve.signals import SignalGenerator


def test_rr_generation_length():
    gen = SignalGenerator(sampling_rate=100)
    rr = gen.generate_rr_intervals(vagal_tone=0.7, sympathetic_tone=0.2, duration_sec=10.0)
    assert len(rr) > 0
    assert isinstance(rr, np.ndarray)


def test_vagal_hrv_effect():
    gen = SignalGenerator()
    # High vagal tone should produce higher standard deviation in RR intervals
    rr_high_vagal = gen.generate_rr_intervals(vagal_tone=0.9, sympathetic_tone=0.1)
    rr_low_vagal = gen.generate_rr_intervals(vagal_tone=0.1, sympathetic_tone=0.9)

    assert np.std(rr_high_vagal) > np.std(rr_low_vagal)
