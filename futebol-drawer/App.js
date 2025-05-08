import 'react-native-gesture-handler';
import * as React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createDrawerNavigator } from '@react-navigation/drawer';
import EscudoScreen from './screens/EscudoScreen';
import JogadoresScreen from './screens/JogadoresScreen';
import TitulosScreen from './screens/TitulosScreen';
import { Provider as PaperProvider, MD3DarkTheme } from 'react-native-paper';
import Ionicons from '@expo/vector-icons/Ionicons';
import CustomDrawerContent from './components/CustomDrawerContent';

const Drawer = createDrawerNavigator();

const theme = {
  ...MD3DarkTheme,
  colors: {
    ...MD3DarkTheme.colors,
    primary: '#D32F2F',
    secondary: '#000000',
  },
};

export default function App() {
  return (
    <PaperProvider theme={theme}>
      <NavigationContainer>
        <Drawer.Navigator
          initialRouteName="Escudo"
          drawerContent={(props) => <CustomDrawerContent {...props} />}
          screenOptions={({ route }) => ({
            drawerActiveTintColor: '#D32F2F',
            drawerInactiveTintColor: '#fff',
            drawerStyle: { backgroundColor: '#121212' },
            headerStyle: { backgroundColor: '#D32F2F' },
            headerTintColor: '#fff',
            headerTitleAlign: 'center',
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