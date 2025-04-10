import React from 'react';
import { View, Image, StyleSheet } from 'react-native';
import { Text } from 'react-native-paper';

const EscudoScreen = ({ escudo, nome }) => (
  <View style={styles.container}>
    <Text variant="titleLarge">{nome}</Text>
    <Image source={{ uri: escudo }} style={styles.escudo} resizeMode="contain" />
  </View>
);

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center',backgroundColor: '#4f4f4f' },
  escudo: { width: 200, height: 200, marginTop: 20, borderRadius: 10 },
});

export default EscudoScreen;
