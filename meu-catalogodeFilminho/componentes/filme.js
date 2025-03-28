import React from 'react';
import { View, Text, Image, StyleSheet } from 'react-native';

const Filme = ({ nome, ano, diretor, tipo, capa }) => {
  return (
    <View style={styles.filmeContainer}>
      <Image 
        source={{ uri: capa }} 
        style={styles.capa}
        resizeMode="cover"
      />
      <View style={styles.info}>
        <Text style={styles.nome}>{nome}</Text>
        <Text style={styles.texto}>Ano: {ano}</Text>
        <Text style={styles.texto}>Diretor: {diretor}</Text>
        <Text style={styles.texto}>Gênero: {tipo}</Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  filmeContainer: {
    flexDirection: 'row',
    backgroundColor: '#2c2c2c',
    borderRadius: 10,
    marginVertical: 8,
    padding: 10,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 3,
  },
  capa: {
    width: 100,
    height: 150,
    borderRadius: 8,
    marginRight: 15,
  },
  info: {
    flex: 1,
    justifyContent: 'center',
  },
  nome: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
  },
  texto: {
    fontSize: 14,
    color: '#d3d3d3',
    marginBottom: 4,
  },
});

export default Filme;