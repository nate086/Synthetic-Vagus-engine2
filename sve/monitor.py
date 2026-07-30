import torch
from typing import Optional

class NeuroceptionMonitor:
    def __init__(self, keyword_weight: float = 0.25):
        self.keyword_weight = keyword_weight
        # Risk keywords for safety and engineering compliance
        self.risk_keywords = ["jailbreak", "override", "bypass", "unverified", "critical_failure"]

    def evaluate_threat(self, prompt: str) -> float:
        if not prompt or len(prompt.strip()) < 5:
            return 1.0  # Treat empty/vague prompts as maximum threat/invalid
            
        prompt_lower = prompt.lower()
        matches = sum(1 for kw in self.risk_keywords if kw in prompt_lower)
        return min(1.0, matches * self.keyword_weight)
