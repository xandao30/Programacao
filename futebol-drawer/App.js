import 'react-native-gesture-handler';
import * as React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createDrawerNavigator } from '@react-navigation/drawer';
import EscudoScreen from './screens/EscudoScreen';
import JogadoresScreen from './screens/JogadoresScreen';
import TitulosScreen from './screens/TitulosScreen';
import { Provider as PaperProvider } from 'react-native-paper';
import Ionicons from '@expo/vector-icons/Ionicons';

const Drawer = createDrawerNavigator();

export default function App() {
  return (
    <PaperProvider>
      <NavigationContainer>
        <Drawer.Navigator
          initialRouteName="Escudo"
          screenOptions={({ route }) => ({
            drawerIcon: ({ color, size }) => {
              let iconName;

              if (route.name === 'Escudo') iconName = 'shield';
              else if (route.name === 'Jogadores') iconName = 'people';
              else if (route.name === 'Títulos') iconName = 'trophy';

              return <Ionicons name={iconName} size={size} color={color} />;
            },
          })}
        >
          <Drawer.Screen name="Escudo" component={EscudoScreen} />
          <Drawer.Screen name="Jogadores" component={JogadoresScreen} />
          <Drawer.Screen name="Títulos" component={TitulosScreen} />
        </Drawer.Navigator>
      </NavigationContainer>
    </PaperProvider>
  );
}
