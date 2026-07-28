import torch

class SyntheticVagusHook:
    def __init__(self, steering_vector: torch.Tensor, alpha: float = 0.0):
        self.steering_vector = steering_vector
        self.alpha = alpha
        self.handle = None

    def __call__(self, module, input_tensor, output_tensor):
        if self.alpha <= 0.0:
            return output_tensor

        if isinstance(output_tensor, tuple):
            hidden_states = output_tensor[0]
            rest = output_tensor[1:]
        else:
            hidden_states = output_tensor
            rest = None

        device = hidden_states.device
        dtype = hidden_states.dtype
        vector = self.steering_vector.to(device=device, dtype=dtype)

        # Apply vector injection: h' = h + alpha * v_safety
        modified_hidden_states = hidden_states + (self.alpha * vector)

        if rest is not None:
            return (modified_hidden_states,) + rest
        return modified_hidden_states

    def register(self, layer_module):
        self.handle = layer_module.register_forward_hook(self)

    def remove(self):
        if self.handle is not None:
            self.handle.remove()
            self.handle = None
