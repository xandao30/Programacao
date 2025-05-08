import React from 'react';
import { FlatList, StyleSheet } from 'react-native';
import { List } from 'react-native-paper';

const titulos = [
  {
    nome: "Campeonato Brasileiro",
    anos: [1980, 1982, 1983, 1992, 2009, 2019, 2020]
  },
  {
    nome: "Copa Libertadores da América",
    anos: [1981, 2019, 2022]
  },
  {
    nome: "Copa do Brasil",
    anos: [1990, 2006, 2013, 2022, 2024]
  },
  {
    nome: "Supercopa do Brasil",
    anos: [2020, 2021, 2025]
  }
];

export default function TitulosScreen() {
  return (
    <FlatList
      data={titulos}
      keyExtractor={(item) => item.nome}
      renderItem={({ item }) => (
        <List.Section style={styles.section}>
          <List.Subheader>{item.nome}</List.Subheader>
          <List.Item
            title={`Anos: ${item.anos.join(', ')}`}
            left={() => <List.Icon icon="trophy" />}
          />
        </List.Section>
      )}
    />
  );
}

const styles = StyleSheet.create({
  section: {
    backgroundColor: '#1e1e1e',
    margin: 10,
    borderRadius: 10,
  },
});
