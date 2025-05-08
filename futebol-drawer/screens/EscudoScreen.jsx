import React from 'react';
import { View, Image, StyleSheet } from 'react-native';
import { Card, Text } from 'react-native-paper';

const time = {
  nome: "Flamengo",
  escudo: "https://i.pinimg.com/236x/16/db/d2/16dbd20fd582e025dc54cc3fbd1839c9.jpg",
  fundacao: "15 de novembro de 1895",
  estadio: "Maracanã",
  mascote: "Urubu",
  cores: ["Vermelho", "Preto"]
};

export default function EscudoScreen() {
  return (
    <View style={styles.container}>
      <Card>
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
});
