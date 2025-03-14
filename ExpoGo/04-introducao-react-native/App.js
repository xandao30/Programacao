//Imports
import { StatusBar } from 'expo-status-bar';
import { Button, StyleSheet, Text, View, Image } from 'react-native';

//Componente Principal
//Ele deve retornar o que será renderizado na tela (Template feito com JSX)
export default function App() {
    //Logica do meu componente
  const nome = "Jhon"

  function Alerta () {
    alert("Voce clicou no botao alerta!")
  }

    //Retorno com JSX
  return (
    <View style={styles.container}>


    <Text>{2+2}</Text>
    <Text>{nome}</Text>
    <Text>Testando</Text>
    <Image
    source={{uri: 'https://blogdoarmindo.com.br/wp-content/uploads/2024/05/2c71f7fc1a57010f17beb9d1841060e1.jpg' }}
    style={{
      height:250,
      width:300
    }}
    />


    <Button title='teste' color="#841584" onPress={Alerta}></Button>

      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
