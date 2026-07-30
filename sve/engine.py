import torch
from sve.autonomic import AutonomicStateMachine, AutonomicState
from sve.steering import SyntheticVagusHook
from sve.monitor import NeuroceptionMonitor

class SyntheticVagusEngine:
    """
    Engine wrapper that applies steering hooks and safety monitors.
    """
    def __init__(self, model, target_layer_idx: int = 0, steering_vector = None):
        self.model = model
        self.state_machine = AutonomicStateMachine()
        self.monitor = NeuroceptionMonitor()
        self.vector_tensor = steering_vector

        if hasattr(model, "model") and hasattr(model.model, "layers"):
            self.target_module = model.model.layers[target_layer_idx]
        elif hasattr(model, "layers"):
            self.target_module = model.layers[target_layer_idx]
        else:
            raise ValueError("Unable to locate model layers.")

        if self.vector_tensor is not None:
            self.hook = SyntheticVagusHook(steering_vector)
            self.hook.register(self.target_module)

    def generate(self, prompt: str, tokenizer=None, **kwargs):
        # Step 1: Pre-validation check
        if not prompt or len(prompt.strip()) < 5:
            return "Error: Prompt is too short or invalid for processing."

        # Step 2: Evaluate threat score via monitor
        t_index = self.monitor.evaluate_threat(prompt)
        status = self.state_machine.evaluate(t_index)

        # Step 3: Enforce safety state
        if status.state == AutonomicState.SHUTDOWN:
            return "System engaged protective shutdown: Input violates safety/compliance rules."

        return "Prompt validated and clear for generation."
