export interface Sve2MarketState {
  sveScore: number;       // -1.0 (Strong PUT) to +1.0 (Strong CALL)
  entropy: number;        // Signal strength (0.0 to 1.0)
  ppmBlocked: boolean;    // Safety shield (True if volatility spike)
  recommendedAction: 'CALL' | 'PUT' | 'HOLD';
}

export class MarketSve2Engine {
  private tickHistory: number[] = [];
  private readonly maxWindow: number = 30; // 30-tick rolling window

  // PPM Safety Parameters
  private readonly maxVolatilityDelta: number = 0.004; // 0.4% spike cap
  private readonly minEntropyThreshold: number = 0.30; // Noise filter

  /**
   * Main Sub-Millisecond Processing Loop
   */
  public ingestTick(price: number): Sve2MarketState {
    this.tickHistory.push(price);
    if (this.tickHistory.length > this.maxWindow) {
      this.tickHistory.shift();
    }

    // 1. Calculate SVE2 Directional Bias & Entropy
    const { sveScore, entropy } = this.calculateSve2Steering();

    // 2. Evaluate PPM Safety Envelope
    const ppmBlocked = this.evaluatePpmShield(price);

    // 3. Determine Final Output
    let recommendedAction: 'CALL' | 'PUT' | 'HOLD' = 'HOLD';

    if (!ppmBlocked && entropy >= this.minEntropyThreshold) {
      if (sveScore > 0.4) recommendedAction = 'CALL';
      else if (sveScore < -0.4) recommendedAction = 'PUT';
    }

    return {
      sveScore,
      entropy,
      ppmBlocked,
      recommendedAction,
    };
  }

  private calculateSve2Steering(): { sveScore: number; entropy: number } {
    if (this.tickHistory.length < 5) return { sveScore: 0, entropy: 0 };

    let directionalSum = 0;
    let absoluteSum = 0;

    for (let i = 1; i < this.tickHistory.length; i++) {
      const delta = this.tickHistory[i] - this.tickHistory[i - 1];
      directionalSum += delta;
      absoluteSum += Math.abs(delta);
    }

    if (absoluteSum === 0) return { sveScore: 0, entropy: 0 };

    const sveScore = directionalSum / absoluteSum;
    return { sveScore, entropy: Math.abs(sveScore) };
  }

  private evaluatePpmShield(currentPrice: number): boolean {
    if (this.tickHistory.length < 2) return false;
    const basePrice = this.tickHistory[0];
    const volatility = Math.abs(currentPrice - basePrice) / basePrice;
    return volatility > this.maxVolatilityDelta;
  }
}
