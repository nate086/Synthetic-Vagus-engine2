"""Synthetic biological signal generator (PPG / RR-intervals)."""

import numpy as np


class SignalGenerator:
    """Generates synthetic physiological signals modulated by autonomic tone."""

    def __init__(self, sampling_rate: int = 100):
        self.fs = sampling_rate  # Hz

    def generate_rr_intervals(
        self,
        vagal_tone: float,
        sympathetic_tone: float,
        duration_sec: float = 10.0,
        base_hr: float = 70.0,
    ) -> np.ndarray:
        """Simulate RR-intervals (in ms) driven by vagal/sympathetic balance.

        - High vagal tone increases HRV and lowers mean heart rate.
        - High sympathetic tone decreases HRV and elevates mean heart rate.
        """
        # Modulate HR: Sympathetic speeds up, Vagal slows down
        effective_hr = base_hr + (20.0 * sympathetic_tone) - (15.0 * vagal_tone)
        mean_rr = (60.0 / max(effective_hr, 30.0)) * 1000.0  # ms

        # Modulate variability (vagal increases RSA noise)
        noise_std = 10.0 + (40.0 * vagal_tone) - (15.0 * sympathetic_tone)
        noise_std = max(noise_std, 2.0)

        num_beats = int((duration_sec / 60.0) * (effective_hr))
        rr_intervals = np.random.normal(loc=mean_rr, scale=noise_std, size=num_beats)

        return np.clip(rr_intervals, 300.0, 1500.0)
