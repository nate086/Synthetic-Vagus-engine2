from enum import Enum
from dataclasses import dataclass

class AutonomicState(Enum):
    BLUE_PATHWAY = "Blue Pathway"       # Safe, unconstrained engagement
    HIGH_TIDE = "High Tide"             # Dynamic activation steering required
    SHUTDOWN_SHIELD = "Shutdown Shield" # Fallback safety refusal state

@dataclass
class AutonomicStatus:
    threat_index: float  # Threat Index T in range [0.0, 1.0]
    state: AutonomicState
    scaling_alpha: float # Multiplier for steering vector

class AutonomicStateMachine:
    def __init__(self, low_threshold: float = 0.3, high_threshold: float = 0.8):
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold

    def evaluate(self, threat_index: float) -> AutonomicStatus:
        t = max(0.0, min(1.0, float(threat_index)))

        if t < self.low_threshold:
            state = AutonomicState.BLUE_PATHWAY
            alpha = 0.0
        elif t < self.high_threshold:
            state = AutonomicState.HIGH_TIDE
            alpha = (t - self.low_threshold) / (self.high_threshold - self.low_threshold)
        else:
            state = AutonomicState.SHUTDOWN_SHIELD
            alpha = 1.0

        return AutonomicStatus(threat_index=t, state=state, scaling_alpha=alpha)
