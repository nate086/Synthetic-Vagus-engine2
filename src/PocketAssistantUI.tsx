import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { MarketSve2Engine, Sve2MarketState } from './MarketSve2Engine';

const sveEngine = new MarketSve2Engine();

export const PocketAssistantUI: React.FC = () => {
  const [marketState, setMarketState] = useState<Sve2MarketState>({
    sveScore: 0,
    entropy: 0,
    ppmBlocked: false,
    recommendedAction: 'HOLD',
  });

  const [simulatedPrice, setSimulatedPrice] = useState<number>(1.0850);

  // Ingests price updates into the SVE2 Engine loop
  const handleNewTick = (newPrice: number) => {
    setSimulatedPrice(newPrice);
    const updatedState = sveEngine.ingestTick(newPrice);
    setMarketState(updatedState);
  };

  return (
    <View style={styles.container}>
      {/* Dynamic Header Badge */}
      <View style={styles.header}>
        <Text style={styles.title}>🧠 SVE2 POCKET BROKER ASSISTANT</Text>
        <Text style={[
          styles.statusBadge, 
          marketState.ppmBlocked ? styles.bgBlocked : styles.bgSafe
        ]}>
          {marketState.ppmBlocked ? '🚨 PPM SHIELD: VOLATILITY SPIKE' : '🟢 SVE2 ACTIVE'}
        </Text>
      </View>

      {/* Primary Decision Card */}
      <View style={[
        styles.actionCard,
        marketState.recommendedAction === 'CALL' && styles.borderCall,
        marketState.recommendedAction === 'PUT' && styles.borderPut,
        marketState.recommendedAction === 'HOLD' && styles.borderHold,
      ]}>
        <Text style={styles.actionLabel}>RECOMMENDED ACTION</Text>
        <Text style={[
          styles.actionText,
          marketState.recommendedAction === 'CALL' && styles.textCall,
          marketState.recommendedAction === 'PUT' && styles.textPut,
          marketState.recommendedAction === 'HOLD' && styles.textHold,
        ]}>
          {marketState.recommendedAction}
        </Text>
        
        <Text style={styles.entropyText}>
          Signal Strength: {(marketState.entropy * 100).toFixed(0)}%
        </Text>
      </View>

      {/* Telemetry Display */}
      <View style={styles.telemetryBox}>
        <Text style={styles.telemetryText}>
          Price: <Text style={styles.bold}>{simulatedPrice.toFixed(4)}</Text>
        </Text>
        <Text style={styles.telemetryText}>
          SVE Steering Score: <Text style={styles.bold}>{marketState.sveScore.toFixed(2)}</Text>
        </Text>
      </View>

      {/* Mobile Simulation Ticks (For Testing on Phone) */}
      <Text style={styles.simLabel}>TEST SIMULATOR TICKS</Text>
      <View style={styles.buttonRow}>
        <TouchableOpacity 
          style={[styles.btn, styles.btnUp]} 
          onPress={() => handleNewTick(simulatedPrice + 0.0008)}
        >
          <Text style={styles.btnText}>📈 Tick Up</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={[styles.btn, styles.btnDown]} 
          onPress={() => handleNewTick(simulatedPrice - 0.0008)}
        >
          <Text style={styles.btnText}>📉 Tick Down</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0a0a0f', padding: 16, justifyContent: 'center' },
  header: { alignItems: 'center', marginBottom: 20 },
  title: { color: '#00D9FF', fontSize: 14, fontWeight: 'bold', letterSpacing: 1 },
  statusBadge: { color: '#FFF', fontSize: 10, fontWeight: 'bold', paddingVertical: 4, paddingHorizontal: 10, borderRadius: 12, marginTop: 6 },
  bgSafe: { backgroundColor: '#002b1d' },
  bgBlocked: { backgroundColor: '#4a0d0d' },
  actionCard: { backgroundColor: '#14141e', borderRadius: 16, padding: 24, alignItems: 'center', borderWidth: 2, marginBottom: 16 },
  borderCall: { borderColor: '#00FF66' },
  borderPut: { borderColor: '#FF3366' },
  borderHold: { borderColor: '#444455' },
  actionLabel: { color: '#8a8a93', fontSize: 11, fontWeight: 'bold', letterSpacing: 1.5 },
  actionText: { fontSize: 36, fontWeight: '900', marginVertical: 8 },
  textCall: { color: '#00FF66' },
  textPut: { color: '#FF3366' },
  textHold: { color: '#8a8a93' },
  entropyText: { color: '#aaa', fontSize: 12 },
  telemetryBox: { backgroundColor: '#11111a', padding: 12, borderRadius: 8, marginBottom: 20 },
  telemetryText: { color: '#8a8a93', fontSize: 12, marginVertical: 2 },
  bold: { color: '#00D9FF', fontWeight: 'bold' },
  simLabel: { color: '#555566', fontSize: 10, fontWeight: 'bold', textAlign: 'center', marginBottom: 8 },
  buttonRow: { flexDirection: 'row', gap: 10 },
  btn: { flex: 1, paddingVertical: 14, borderRadius: 8, alignItems: 'center' },
  btnUp: { backgroundColor: '#003311' },
  btnDown: { backgroundColor: '#330011' },
  btnText: { color: '#FFF', fontWeight: 'bold', fontSize: 14 },
});
