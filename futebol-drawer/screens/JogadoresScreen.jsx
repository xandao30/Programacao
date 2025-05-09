import React from 'react';
import { FlatList, StyleSheet } from 'react-native';
import { Card, Text } from 'react-native-paper';

const jogadores = [
  {
    nome: "Stephen Curry",
    numero: 30,
    posicao: "Armador",
    idade: 36,
    imagem: "https://cdn.nba.com/headshots/nba/latest/1040x760/201939.png"
  },
  {
    nome: "Klay Thompson",
    numero: 11,
    posicao: "Ala-armador",
    idade: 34,
    imagem: "https://cdn.nba.com/headshots/nba/latest/1040x760/202691.png"
  },
  {
    nome: "Draymond Green",
    numero: 23,
    posicao: "Ala-pivô",
    idade: 34,
    imagem: "https://cdn.nba.com/headshots/nba/latest/1040x760/203110.png"
  },
  {
    nome: "Andrew Wiggins",
    numero: 22,
    posicao: "Ala",
    idade: 29,
    imagem: "https://cdn.nba.com/headshots/nba/latest/1040x760/203952.png"
  },
  {
    nome: "Kevon Looney",
    numero: 5,
    posicao: "Pivô",
    idade: 28,
    imagem: "https://cdn.nba.com/headshots/nba/latest/1040x760/1626172.png"
  }
];

export default function JogadoresScreen() {
  return (
    <FlatList
      data={jogadores}
      keyExtractor={(item) => item.nome}
      renderItem={({ item }) => (
        <Card style={styles.card}>
          <Card.Title title={item.nome} subtitle={item.posicao} />
          <Card.Content>
            <Text>Número: {item.numero}</Text>
            <Text>Idade: {item.idade}</Text>
          </Card.Content>
          <Card.Cover source={{ uri: item.imagem }} />
        </Card>
      )}
    />
  );
}

const styles = StyleSheet.create({
  card: {
    margin: 10,
    borderRadius: 12,
    elevation: 4,
    backgroundColor: '#1e1e1e',
  },
});
