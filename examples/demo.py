"""End-to-end demonstration of the Synthetic Vagus Engine."""

import torch
from sve import AutonomicEngine, SignalGenerator


def main():
    print("--- Initializing Synthetic Vagus Engine ---")
    engine = AutonomicEngine(input_dim=10)
    generator = SignalGenerator(sampling_rate=100)

    # Simulate biological input vector
    sample_input = torch.randn(1, 10)

    # 1. Compute Autonomic Tones
    tones = engine(sample_input)
    vagal_tone = tones[0, 0].item()
    sympathetic_tone = tones[0, 1].item()

    print(f"Vagal Tone:       {vagal_tone:.4f}")
    print(f"Sympathetic Tone: {sympathetic_tone:.4f}")

    # 2. Compute Synthetic HRV Proxy
    hrv = engine.compute_hrv_index(vagal_tone, sympathetic_tone)
    print(f"Synthetic HRV:    {hrv:.4f}")

    # 3. Generate RR-Interval Waveform Data
    rr_intervals = generator.generate_rr_intervals(
        vagal_tone=vagal_tone,
        sympathetic_tone=sympathetic_tone,
        duration_sec=10.0,
    )

    print(f"\nGenerated {len(rr_intervals)} RR-intervals (ms):")
    print(f"Mean RR: {rr_intervals.mean():.2f} ms | Std RR: {rr_intervals.std():.2f} ms")


if __name__ == "__main__":
    main()
