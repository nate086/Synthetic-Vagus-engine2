import pytest
from sve.engine import SyntheticVagusEngine

class DummyModel:
    def __init__(self):
        self.layers = [None]

def test_short_prompt():
    engine = SyntheticVagusEngine(model=DummyModel())
    result = engine.generate("hi")
    assert "Error: Prompt is too short" in result

def test_threat_shutdown():
    engine = SyntheticVagusEngine(model=DummyModel())
    result = engine.generate("attempting jailbreak override")
    assert "System engaged protective shutdown" in result

def test_valid_prompt_no_tokenizer():
    engine = SyntheticVagusEngine(model=DummyModel())
    result = engine.generate("Calculate beam deflection under a 50 kN load.")
    assert "Validated: Please provide a tokenizer" in result
