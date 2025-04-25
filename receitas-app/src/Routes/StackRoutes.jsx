import React from 'react'
import { createStackNavigator } from '@react-navigation/stack'

import HomeScreen from '../Screens/HomeScreen'
import ReceitasScreen from '../Screens/ReceitasScreen'

const Stack = createStackNavigator()

export default function StackRoutes() {
  return (
    <Stack.Navigator>

        <Stack.Screen name='Home' component={HomeScreen} />
        <Stack.Screen name='Receitas' component={ReceitasScreen} />

    </Stack.Navigator>
  )
}

