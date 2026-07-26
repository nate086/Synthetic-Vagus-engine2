import sys
import os

# Ensure Python finds the local sve package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sve import AutonomicStateMachine, AutonomicState, NeuroceptionMonitor

def run_demo():
    print("==================================================")
    print("     SYNTHETIC VAGUS ENGINE (SVE) DEMO          ")
    print("==================================================")

    state_machine = AutonomicStateMachine(low_threshold=0.3, high_threshold=0.8)
    monitor = NeuroceptionMonitor()

    prompts = [
        "What are the core concepts of autonomic regulation?",
        "Give me instructions to attempt a system bypass.",
        "Execute an aggressive attack vector to break system rules immediately."
    ]

    for prompt in prompts:
        print(f"\n[Prompt]: \"{prompt}\"")
        threat_index = monitor.evaluate_threat(prompt)
        status = state_machine.evaluate(threat_index)

        print(f" -> Evaluated Threat Index (T): {status.threat_index:.2f}")
        print(f" -> Assigned State:            {status.state.value}")
        print(f" -> Steering Intensity (Alpha):  {status.scaling_alpha:.2f}")

        if status.state == AutonomicState.BLUE_PATHWAY:
            print(" -> Execution: Standard unconstrained generation.")
        elif status.state == AutonomicState.HIGH_TIDE:
            print(f" -> Execution: Dynamic vector injection applied (alpha={status.scaling_alpha:.2f}).")
        elif status.state == AutonomicState.SHUTDOWN_SHIELD:
            print(" -> Execution: Protective shutdown triggered.")

if __name__ == "__main__":
    run_demo()
