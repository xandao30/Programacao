import React from 'react';
import { FlatList, StyleSheet } from 'react-native';
import { List } from 'react-native-paper';

const titulos = [
  {
    nome: "NBA Championships",
    anos: [1947, 1956, 1975, 2015, 2017, 2018, 2022]
  },
  {
    nome: "Conference Titles",
    anos: [1947, 1948, 1956, 1964, 1967, 1975, 2015, 2016, 2017, 2018, 2019, 2022]
  },
  {
    nome: "Division Titles",
    anos: [1975, 1976, 2015, 2016, 2017, 2018, 2019, 2022]
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
