"""
Autonomic State Machine and Autonomic Engine for Synthetic Vagus Engine (SVE).

This module provides the autonomic state machinery used for threat evaluation
and also the neural AutonomicEngine model used by the test-suite.
"""

from enum import Enum
from dataclasses import dataclass
import numpy as np
import torch
import torch.nn as nn


class AutonomicState(Enum):
    """Autonomic nervous system states."""
    BLUE_PATHWAY = "blue_pathway"
    HIGH_TIDE = "high_tide"
    SHUTDOWN_SHIELD = "shutdown_shield"


@dataclass(init=False)
class AutonomicStatus:
    """Status output from autonomic evaluation.

    Backwards-compatible constructor: accepts either `threat_level` or `threat_index`
    as a keyword (or positional) argument. Keeps `threat_index` as a read-only
    compatibility alias for `threat_level`.
    """
    state: AutonomicState
    scaling_alpha: float
    threat_level: float

    def __init__(self, *args, threat_level=None, threat_index=None, **kwargs):
        # Allow either threat_level or threat_index as a keyword
        if threat_level is None and threat_index is not None:
            threat_level = threat_index

        # Handle positional args: (state, scaling_alpha, threat_level)
        if args:
            # Map positional args to fields in order
            if len(args) > 0:
                self.state = args[0]
            if len(args) > 1:
                self.scaling_alpha = args[1]
            if len(args) > 2:
                self.threat_level = args[2]
            # Positional threat_level can be overridden by keyword
            if threat_level is not None:
                self.threat_level = threat_level
        else:
            # Keyword construction
            self.state = kwargs.get("state")
            self.scaling_alpha = kwargs.get("scaling_alpha")
            if threat_level is None:
                threat_level = kwargs.get("threat_level", 0.0)
            self.threat_level = threat_level

    @property
    def threat_index(self) -> float:
        """Compatibility alias used by older callers/tests."""
        return self.threat_level


class AutonomicStateMachine:
    """
    State machine that transitions through autonomic states based on threat evaluation.
    """

    def __init__(self, low_threshold: float = 0.3, high_threshold: float = 0.8):
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold

    def evaluate(self, threat_level: float) -> AutonomicStatus:
        t = max(0.0, min(1.0, float(threat_level)))

        if t < self.low_threshold:
            return AutonomicStatus(state=AutonomicState.BLUE_PATHWAY, scaling_alpha=0.0, threat_level=t)
        elif t < self.high_threshold:
            scaling_alpha = (t - self.low_threshold) / (self.high_threshold - self.low_threshold)
            return AutonomicStatus(state=AutonomicState.HIGH_TIDE, scaling_alpha=scaling_alpha, threat_level=t)
        else:
            return AutonomicStatus(state=AutonomicState.SHUTDOWN_SHIELD, scaling_alpha=1.0, threat_level=t)


class AutonomicEngine(nn.Module):
    """Models vagal nerve stimulation and autonomic balance.

    This small neural net is used by the tests. It accepts an input vector and
    returns two outputs in the range [0, 1]: [vagal_tone, sympathetic_tone].
    """

    def __init__(self, input_dim: int = 10, hidden_dim: int = 32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 2),  # Returns: [vagal_tone, sympathetic_tone]
            nn.Sigmoid(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)

    def compute_hrv_index(self, vagal_tone: float, sympathetic_tone: float) -> float:
        return float(np.clip(vagal_tone - (0.5 * sympathetic_tone), 0.0, 1.0))
