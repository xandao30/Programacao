import React from 'react';
import { StyleSheet } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { Provider as PaperProvider } from 'react-native-paper';
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';

import EscudoScreen from './screens/escudoscreen.jsx';
import JogadoresScreen from './screens/jogadoresscreen.jsx';
import TitulosScreen from './screens/tituloscreen.jsx';

const Tab = createBottomTabNavigator();

const time = {
  nome: "Flamengo",
  escudo: "https://i.pinimg.com/236x/16/db/d2/16dbd20fd582e025dc54cc3fbd1839c9.jpg",
};

const App = () => {
  return (
    <PaperProvider>
      <SafeAreaProvider>
        <NavigationContainer>
          <SafeAreaView style={styles.container} edges={['top', 'left', 'right']}>
            <Tab.Navigator
              screenOptions={({ route }) => ({
                tabBarIcon: ({ color, size }) => {
                  let iconName;
                  if (route.name === 'Escudo') iconName = 'shield';
                  else if (route.name === 'Jogadores') iconName = 'account-group';
                  else if (route.name === 'Títulos') iconName = 'trophy-outline';

                  return <Icon name={iconName} color={color} size={size} />;
                },
                tabBarActiveTintColor: '#d32f2f',
                tabBarInactiveTintColor: 'gray',
                headerShown: false,
              })}
            >
              <Tab.Screen name="Escudo">
                {() => <EscudoScreen escudo={time.escudo} nome={time.nome} />}
              </Tab.Screen>
              <Tab.Screen name="Jogadores" component={JogadoresScreen} />
              <Tab.Screen name="Títulos" component={TitulosScreen} />
            </Tab.Navigator>
          </SafeAreaView>
        </NavigationContainer>
      </SafeAreaProvider>
    </PaperProvider>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#212121',
  },
});

export default App;
