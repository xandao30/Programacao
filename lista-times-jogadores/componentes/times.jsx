import React from 'react';
import { View, Text, Image, FlatList, StyleSheet } from 'react-native';
import { Card } from 'react-native-paper';
import Jogador from './jogadores.jsx';

const Time = ({ nome, anoFundacao, mascote, imagem, jogadores }) => {
  return (
    <Card style={styles.card}>
      <View style={styles.header}>
        <Image source={{ uri: imagem }} style={styles.timeImage} />
        <View style={styles.info}>
          <Text style={styles.nome}>{nome}</Text>
          <Text style={styles.detalhe}>Fundação: {anoFundacao}</Text>
          <Text style={styles.detalhe}>Mascote: {mascote}</Text>
        </View>
      </View>
      <Text style={styles.jogadoresTitle}>Jogadores:</Text>
      <FlatList
        data={jogadores}
        renderItem={({ item }) => <Jogador {...item} />}
        keyExtractor={item => item.nome}
        horizontal
        showsHorizontalScrollIndicator={false}
      />
    </Card>
  );
};

const styles = StyleSheet.create({
  card: {
    marginBottom: 15,
    padding: 10,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  timeImage: {
    width: 80,
    height: 80,
    borderRadius: 40,
    marginRight: 10,
  },
  info: {
    flex: 1,
  },
  nome: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
  },
  detalhe: {
    fontSize: 14,
    color: '#666',
  },
  jogadoresTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginTop: 10,
    marginBottom: 5,
    color: '#333',
  },
});

export default Time;