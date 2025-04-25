import { StyleSheet, Text, View, FlatList, Image } from 'react-native';
import React from 'react';
import { PaperProvider, Card } from 'react-native-paper';
import { Button } from 'react-native-paper';


export default function ReceitasScreen({navigation, route}) {
    
    console.log("PARAMS => ", route.params)

  return (
    <PaperProvider>
      <View style={styles.container}>
        <Text style={styles.title}>Receitas</Text>
            <Card style={{margin:10}}>
                <Card.Cover source={{uri: route.params.imagem}} style={{height: 200, width:300}}/>
                <Card.Content>
                    <Text style={styles.nome}>{route.params.nome}</Text>
                    <Text>{`Tempo de preparo: ${route.params.tempoPreparo}`}</Text>
                    <Text>{`Porções: ${route.params.porcoes}`}</Text>
                    <Text style={styles.info}>{`Porções: ${route.params.ingredientes}`}</Text>
                    <Text style={styles.info}>{`Porções: ${route.params.modoPreparo}`}</Text>
                    
                </Card.Content>
            </Card>
            <Button
            mode='contained'
            onPress={()=> navigation.goBack()}
        >
            voltar
        </Button>
      </View>
    </PaperProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    flex: 1,
    padding: 10
  },
  title: {
    fontSize: 30,
    marginBottom: 20,
  },
  nome: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  info: {
    fontSize: 14,
    marginBottom: 5,
    color: 'gray',
  },
});
