import React from 'react';
import { FlatList, View, Image } from 'react-native';
import { Card, Text } from 'react-native-paper';

const jogadores = [/* use o array do PDF aqui */];

export default function JogadoresScreen() {
  return (
    <FlatList
      data={jogadores}
      keyExtractor={(item) => item.nome}
      renderItem={({ item }) => (
        <Card style={{ margin: 10 }}>
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
