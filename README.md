# Synthetic-Vagus-Engine (SVE)

A lightweight safety and validation framework designed for AI model steering, threat monitoring, and structural engineering guardrails.

## Features

- **Pre-Generation Threat Monitoring (`monitor.py`):** Automatically detects invalid inputs, jailbreak attempts, and missing structural context before model execution.
- **Autonomic State Machine (`autonomic.py`):** Dynamically triggers protective shutdowns when threat thresholds are exceeded.
- **Real Model Generation (`engine.py`):** Seamlessly integrates with PyTorch and Hugging Face models/tokenizers with custom steering hooks.
- **Engineering Validator (`validator.py`):** Post-processes model outputs to ensure required structural units (e.g., `kN`, `MPa`, `m`) and compliance standards are present.

## Installation

Clone the repository and install dependencies in editable mode:

```bash
git clone [https://github.com/nate086/Synthetic-Vagus-engine2.git](https://github.com/nate086/Synthetic-Vagus-engine2.git)
cd Synthetic-Vagus-engine2
pip install -e .[dev]
