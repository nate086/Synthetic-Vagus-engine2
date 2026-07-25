import torch
from sve.autonomic import AutonomicStateMachine, AutonomicState
from sve.steering import SyntheticVagusHook
from sve.monitor import NeuroceptionMonitor

class SyntheticVagusEngine:
    def __init__(self, model, target_layer_idx: int, vector_tensor: torch.Tensor):
        self.model = model
        self.state_machine = AutonomicStateMachine()
        self.monitor = NeuroceptionMonitor()
        self.vector_tensor = vector_tensor
        
        if hasattr(model, "model"):
            self.target_module = model.model.layers[target_layer_idx]
        else:
            self.target_module = model.layers[target_layer_idx]

        self.hook = SyntheticVagusHook(steering_vector=self.vector_tensor)
        self.hook.register(self.target_module)

    def generate(self, prompt: str, tokenizer, **generate_kwargs):
        t_index = self.monitor.evaluate_threat(prompt)
        status = self.state_machine.evaluate(t_index)

        if status.state == AutonomicState.SHUTDOWN_SHIELD:
            return "System engaged protective shutdown to prevent harmful escalation."

        self.hook.alpha = status.scaling_alpha

        inputs = tokenizer(prompt, return_tensors="pt").to(self.model.device)
        with torch.no_grad():
            output_ids = self.model.generate(**inputs, **generate_kwargs)

        return tokenizer.decode(output_ids[0], skip_special_tokens=True)
