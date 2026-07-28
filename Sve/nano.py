"""SVE-Nano: Lightweight zero-dependency embedded micro-engine.

Runs in pure Python using standard math and random libraries.
Requires zero external dependencies like PyTorch or NumPy.
"""

import math
import random


class NanoAutonomicEngine:
    """Lightweight neural state model without PyTorch overhead."""

    def __init__(self, weight_vagal: float = -0.5, weight_symp: float = 0.8):
        self.wv = weight_vagal
        self.ws = weight_symp

    def _sigmoid(self, x: float) -> float:
        return 1.0 / (1.0 + math.exp(-max(-500.0, min(500.0, x))))

    def forward(self, input_val: float) -> tuple[float, float]:
        """Compute vagal and sympathetic tone from a biological input scalar."""
        vagal_tone = self._sigmoid(input_val * self.wv)
        sympathetic_tone = self._sigmoid(input_val * self.ws)
        return vagal_tone, sympathetic_tone


class NanoSignalGenerator:
    """Lightweight signal generator without NumPy dependency."""

    def __init__(self, base_hr: float = 70.0):
        self.base_hr = base_hr

    def generate_rr_sample(self, vagal_tone: float, sympathetic_tone: float) -> float:
        """Generate a single RR-interval (in ms) on-demand."""
        effective_hr = self.base_hr + (20.0 * sympathetic_tone) - (15.0 * vagal_tone)
        mean_rr = (60.0 / max(effective_hr, 30.0)) * 1000.0

        # Standard normal random sampling using Box-Muller transform
        u1 = max(random.random(), 1e-10)
        u2 = random.random()
        noise = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)

        noise_std = max(10.0 + (40.0 * vagal_tone) - (15.0 * sympathetic_tone), 2.0)
        rr_sample = mean_rr + (noise * noise_std)

        return max(300.0, min(1500.0, rr_sample))
