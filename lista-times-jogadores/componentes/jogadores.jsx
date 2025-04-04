import React from 'react';
import { View, Text, Image, StyleSheet } from 'react-native';
import { Card } from 'react-native-paper';

const Jogador = ({ nome, numero, imagem }) => {
  return (
    <Card style={styles.card}>
      <Image source={{ uri: imagem }} style={styles.imagem} />
      <View style={styles.info}>
        <Text style={styles.nome}>{nome}</Text>
        <Text style={styles.numero}>Nº {numero}</Text>
      </View>
    </Card>
  );
};

const styles = StyleSheet.create({
  card: {
    width: 120,
    marginRight: 10,
    padding: 5,
  },
  imagem: {
    width: 100,
    height: 100,
    borderRadius: 50,
    alignSelf: 'center',
  },
  info: {
    alignItems: 'center',
    marginTop: 5,
  },
  nome: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
  },
  numero: {
    fontSize: 12,
    color: '#666',
  },
});

export default Jogador;