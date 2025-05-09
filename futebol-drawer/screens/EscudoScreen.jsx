import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Card, Text } from 'react-native-paper';

const time = {
  nome: "Golden State Warriors",
  escudo: "https://bolade3.com.br/wp-content/uploads/2022/10/golden-state-scaled.jpg",
  fundacao: "1946",
  estadio: "Chase Center",
  mascote: "Thunder (mascote anterior)",
  cores: ["Azul", "Dourado"]
};

export default function EscudoScreen() {
  return (
    <View style={styles.container}>
      <Card style={styles.card}>
        <Card.Cover source={{ uri: time.escudo }} />
        <Card.Title title={time.nome} subtitle={`Fundado em ${time.fundacao}`} />
        <Card.Content>
          <Text>Estádio: {time.estadio}</Text>
          <Text>Mascote: {time.mascote}</Text>
          <Text>Cores: {time.cores.join(' e ')}</Text>
        </Card.Content>
      </Card>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
  },
  card: {
    borderRadius: 12,
    backgroundColor: '#1e1e1e',
    elevation: 4,
  },
});
