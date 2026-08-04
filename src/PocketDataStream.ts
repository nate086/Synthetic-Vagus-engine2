import { sve2MarketEngine, Sve2MarketState } from './MarketSve2Engine';

export type TickCallback = (state: Sve2MarketState, price: number) => void;

export class PocketDataStream {
  private socket: WebSocket | null = null;
  private isConnected: boolean = false;

  /**
   * Connects to a generic JSON WebSocket tick feed (e.g. Crypto/FX tick stream)
   */
  public connect(wsUrl: string, onTick: TickCallback) {
    try {
      this.socket = new WebSocket(wsUrl);

      this.socket.onopen = () => {
        this.isConnected = true;
        console.log('⚡ SVE2 Market Stream Connected');
      };

      this.socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          // Expecting tick format: { price: number } or custom broker payload
          const price = data.price || data.close || data.p;

          if (typeof price === 'number') {
            const updatedState = sve2MarketEngine.ingestTick(price);
            onTick(updatedState, price);
          }
        } catch (e) {
          // Non-JSON or keepalive heartbeat frame
        }
      };

      this.socket.onerror = (err) => {
        console.warn('SVE2 Stream Error:', err);
      };

      this.socket.onclose = () => {
        this.isConnected = false;
        console.log('SVE2 Market Stream Disconnected');
      };
    } catch (e) {
      console.error('Failed to initialize WebSocket stream:', e);
    }
  }

  public disconnect() {
    if (this.socket) {
      this.socket.close();
      this.isConnected = false;
    }
  }
}

export const pocketStream = new PocketDataStream();
