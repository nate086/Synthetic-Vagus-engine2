"""Autonomic Engine module for Synthetic Vagus Engine (SVE)."""

import numpy as np
import torch
import torch.nn as nn


class AutonomicEngine(nn.Module):
    """Models vagal nerve stimulation and autonomic balance."""

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
