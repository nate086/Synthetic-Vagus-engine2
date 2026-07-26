from typing import Mapping

class NeuroceptionMonitor:
    """
    Minimal NeuroceptionMonitor placeholder.

    Usage:
        monitor = NeuroceptionMonitor()
        score = monitor.evaluate({"heart_rate_variability": 0.3, "skin_conductance": 0.2})
    Returns:
        threat score in [0.0, 1.0] where 0 = no threat, 1 = high threat.
    """

    def __init__(self, weights: Mapping[str, float] | None = None):
        # default weights can be tuned later
        self.weights = dict(weights or {
            "heart_rate_variability": -1.0,  # higher HRV -> lower threat
            "skin_conductance": 1.0,         # higher SC -> higher threat
            "heart_rate": 0.5,
        })

    def evaluate(self, inputs: Mapping[str, float]) -> float:
        if not inputs:
            return 0.0
        score = 0.0
        weight_sum = 0.0
        for k, w in self.weights.items():
            v = float(inputs.get(k, 0.0))
            # normalize heuristically: assume inputs are roughly in [0,1] or can be scaled
            score += w * v
            weight_sum += abs(w)
        if weight_sum == 0:
            return 0.0
        # map to -1..1 then to 0..1 using clamp
        normalized = score / weight_sum
        normalized = max(-1.0, min(1.0, normalized))
        return (normalized + 1.0) / 2.0
