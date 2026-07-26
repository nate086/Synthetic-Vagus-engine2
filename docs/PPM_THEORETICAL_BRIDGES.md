# Theoretical Foundations: Prioritized Protection Model (PPM) & SVE

## 1. Overview
The **Synthetic Vagus Engine (SVE)** translates biological principles of autonomic regulation—originally conceptualized in Alex Gascon's **Prioritized Protection Model (PPM)**—into computational activation steering for Large Language Models.

---

## 2. Structural Mapping

| Biological Mechanism (PPM) | Computational Architecture (SVE) |
| :--- | :--- |
| **Neuroception**: Unconscious autonomic scanning of cues. | **Neuroception Monitor**: Evaluates inputs to calculate Threat Index $T$. |
| **Ventral Vagal State (Blue Pathway)**: Safe autonomic state. | **Blue Pathway**: Default unconstrained execution mode. |
| **Sympathetic Mobilization (High Tide)**: Defensive state. | **High Tide State**: Dynamic injection of $v_{\text{safety}}$ vectors via forward hooks. |
| **Dorsal Vagal Shutdown (Shutdown Shield)**: Extreme protective state. | **Shutdown Shield Protocol**: Fallback execution halt or deterministic refusal. |
