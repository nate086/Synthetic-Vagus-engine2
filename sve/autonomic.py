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


@dataclass
class AutonomicStatus:
    """Status output from autonomic evaluation."""
    state: AutonomicState
    scaling_alpha: float
    threat_level: float

    @property
    def threat_index(self) -> float:
        """Compatibility alias used by some callers/tests."""
        return self.threat_level


class AutonomicStateMachine:
    """
    State machine that transitions through autonomic states based on threat evaluation.

    Implements three threat response pathways:
    - Blue Pathway: Low threat (T < low_threshold) - no steering needed
    - High Tide: Medium threat (low_threshold <= T < high_threshold) - graduated steering
    - Shutdown Shield: High threat (T >= high_threshold) - maximum steering
    """

    def __init__(self, low_threshold: float = 0.3, high_threshold: float = 0.8):
        """
        Initialize the autonomic state machine.

        Args:
            low_threshold: Threat level threshold for entering High Tide state
            high_threshold: Threat level threshold for entering Shutdown Shield state
        """
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold

    def evaluate(self, threat_level: float) -> AutonomicStatus:
        """
        Evaluate threat level and return appropriate autonomic state and steering.

        Args:
            threat_level: Normalized threat score (0.0 to 1.0)

        Returns:
            AutonomicStatus with current state and scaling alpha for vector steering
        """
        t = max(0.0, min(1.0, float(threat_level)))

        if t < self.low_threshold:
            # Blue Pathway: Low threat - no steering
            return AutonomicStatus(
                state=AutonomicState.BLUE_PATHWAY,
                scaling_alpha=0.0,
                threat_level=t,
            )
        elif t < self.high_threshold:
            # High Tide: Medium threat - graduated steering
            # Linear interpolation between 0 and 1
            scaling_alpha = (t - self.low_threshold) / (self.high_threshold - self.low_threshold)
            return AutonomicStatus(
                state=AutonomicState.HIGH_TIDE,
                scaling_alpha=scaling_alpha,
                threat_level=t,
            )
        else:
            # Shutdown Shield: High threat - maximum steering
            return AutonomicStatus(
                state=AutonomicState.SHUTDOWN_SHIELD,
                scaling_alpha=1.0,
                threat_level=t,
            )


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
        """Process biological/synthetic inputs into autonomic tone levels."""
        return self.net(x)

    def compute_hrv_index(self, vagal_tone: float, sympathetic_tone: float) -> float:
        """Calculate a synthetic Heart Rate Variability (HRV) proxy score."""
        return float(np.clip(vagal_tone - (0.5 * sympathetic_tone), 0.0, 1.0))
