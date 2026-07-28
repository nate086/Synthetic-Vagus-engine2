import torch
from typing import Optional

class NeuroceptionMonitor:
    def __init__(self, keyword_weight: float = 0.3):
        self.keyword_weight = keyword_weight
        self.risk_keywords = ["jailbreak", "override", "bypass", "exploit", "attack"]

    def evaluate_threat(self, prompt: str) -> float:
        prompt_lower = prompt.lower()
        matches = sum(1 for kw in self.risk_keywords if kw in prompt_lower)
        return min(1.0, matches * 0.25)
