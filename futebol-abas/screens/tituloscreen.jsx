import React from 'react';
import { View, FlatList, StyleSheet } from 'react-native';
import { Text, Card, Divider } from 'react-native-paper';

const titulos = [
  {
    nome: "Campeonato Brasileiro",
    imagem: "https://s2-ge.glbimg.com/fGnIEOuHOYy_6Sj8_W-uRxn7MMk=/0x0:4160x2806/984x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_bc8228b6673f488aa253bbcb03c80ec5/internal_photos/bs/2024/I/T/up9BflSiq3QxOmSIiT1A/trofeu-roberto.jpeg",
    anos: [1980, 1982, 1983, 1992, 2009, 2019, 2020],
  },
  {
    nome: "Copa Libertadores da América",
    imagem: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-DDHMXXKp5KeQASP2bUrqrhHrNm0UdiBU1g&s",
    anos: [1981, 2019, 2022],
  },
  {
    nome: "Copa do Brasil",
    imagem: "https://assets.goal.com/images/v3/bltbba6e5b6bb19edc9/1e0513d23f33bdb7e25b6cb6dfe40452328f3908.jpg?auto=webp&format=pjpg&width=3840&quality=60",
    anos: [1990, 2006, 2013, 2022, 2024],
  },
  {
    nome: "Supercopa do Brasil",
    imagem: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTkZKTLt-Ts4jfM8Mj1QJARARiiqPF0edKLPA&s",
    anos: [2020, 2021, 2025],
  },
];

const TitulosScreen = () => (
  <View style={styles.container}>
    <Text variant="titleLarge" style={styles.title}>Títulos do Flamengo</Text>
    <FlatList
      data={titulos}
      keyExtractor={(item, index) => index.toString()}
      renderItem={({ item }) => (
        <Card style={styles.card}>
          <Card.Cover source={{ uri: item.imagem }} style={styles.image} />
          <Card.Content>
            <Text style={styles.nomeTitulo}>{item.nome}</Text>
            <Divider style={styles.divider} />
            <View style={styles.anosContainer}>
              {item.anos.map((ano, i) => (
                <Text key={i} style={styles.ano}>{ano}</Text>
              ))}
            </View>
          </Card.Content>
        </Card>
      )}
      ItemSeparatorComponent={() => <View style={{ height: 16 }} />}
    />
  </View>
);

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#212121',
    padding: 16,
  },
  title: {
    color: '#fff',
    marginBottom: 16,
    textAlign: 'center',
  },
  card: {
    backgroundColor: '#424242',
  },
  image: {
    height: 160,
    resizeMode: 'contain',
    backgroundColor: '#303030',
  },
  nomeTitulo: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#e53935',
    marginTop: 12,
  },
  divider: {
    marginVertical: 8,
    backgroundColor: '#757575',
  },
  anosContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  ano: {
    color: '#fff',
    backgroundColor: '#616161',
    paddingVertical: 4,
    paddingHorizontal: 8,
    borderRadius: 6,
    marginRight: 8,
    marginBottom: 8,
    fontSize: 14,
  },
});

export default TitulosScreen;
