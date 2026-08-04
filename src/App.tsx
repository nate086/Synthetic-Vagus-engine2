import React from 'react';
import { SafeAreaView, StatusBar, StyleSheet } from 'react-native';
import { PocketAssistantUI } from './src/PocketAssistantUI';

export default function App() {
  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#0a0a0f" />
      <PocketAssistantUI />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0a0a0f',
  },
});
