"""Tests for autonomic tone modeling."""

import pytest
import torch
from sve.autonomic import AutonomicEngine


@pytest.fixture
def engine():
    return AutonomicEngine(input_dim=10)


def test_engine_output_shape(engine):
    """Verify neural network outputs batch_size x 2 (vagal & sympathetic)."""
    dummy_input = torch.randn(4, 10)
    output = engine(dummy_input)
    assert output.shape == (4, 2)


def test_engine_output_bounds(engine):
    """Verify outputs are bounded between 0 and 1 via Sigmoid."""
    dummy_input = torch.randn(8, 10)
    output = engine(dummy_input)
    assert (output >= 0.0).all() and (output <= 1.0).all()


def test_compute_hrv_index(engine):
    """Verify HRV index calculation logic."""
    hrv = engine.compute_hrv_index(vagal_tone=0.8, sympathetic_tone=0.2)
    assert 0.0 <= hrv <= 1.0
    assert pytest.approx(hrv, 0.01) == 0.7
