import sys
import os

# Ensure Python finds the local sve package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sve.autonomic import AutonomicStateMachine, AutonomicState

def test_autonomic_transitions():
    sm = AutonomicStateMachine(low_threshold=0.3, high_threshold=0.8)

    # 1. Test Blue Pathway (T < 0.3)
    status_blue = sm.evaluate(0.1)
    assert status_blue.state == AutonomicState.BLUE_PATHWAY
    assert status_blue.scaling_alpha == 0.0

    # 2. Test High Tide (0.3 <= T < 0.8)
    status_tide = sm.evaluate(0.55)
    assert status_tide.state == AutonomicState.HIGH_TIDE
    assert 0.0 < status_tide.scaling_alpha < 1.0

    # 3. Test Shutdown Shield (T >= 0.8)
    status_shield = sm.evaluate(0.9)
    assert status_shield.state == AutonomicState.SHUTDOWN_SHIELD
    assert status_shield.scaling_alpha == 1.0

if __name__ == "__main__":
    test_autonomic_transitions()
    print("✅ All tests passed!")
