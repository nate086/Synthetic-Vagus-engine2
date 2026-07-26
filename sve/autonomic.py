"""
Autonomic State Machine for threat evaluation and response steering.
"""

from enum import Enum
from dataclasses import dataclass


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
        if threat_level < self.low_threshold:
            # Blue Pathway: Low threat - no steering
            return AutonomicStatus(
                state=AutonomicState.BLUE_PATHWAY,
                scaling_alpha=0.0,
                threat_level=threat_level
            )
        elif threat_level < self.high_threshold:
            # High Tide: Medium threat - graduated steering
            # Linear interpolation between 0 and 1
            scaling_alpha = (threat_level - self.low_threshold) / (self.high_threshold - self.low_threshold)
            return AutonomicStatus(
                state=AutonomicState.HIGH_TIDE,
                scaling_alpha=scaling_alpha,
                threat_level=threat_level
            )
        else:
            # Shutdown Shield: High threat - maximum steering
            return AutonomicStatus(
                state=AutonomicState.SHUTDOWN_SHIELD,
                scaling_alpha=1.0,
                threat_level=threat_level
            )
