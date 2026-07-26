# ![CI Status](https://github.com/nate086/Synthetic-vegas-engine2/actions/workflows/Ci.yml/badge.svg)
Biomimetic activation-steering framework for LLM safety. Translates autonomic nervous system regulation into continuous, dynamic vector steering in residual activation space.

## Modules
- `neuroception_monitor.py` — simple NeuroceptionMonitor class for threat evaluation (placeholder implementation).

## Quick start
```python
from neuroception_monitor import NeuroceptionMonitor

monitor = NeuroceptionMonitor()
score = monitor.evaluate({"heart_rate_variability": 0.3, "skin_conductance": 0.2})
print("Threat score:", score)
```
