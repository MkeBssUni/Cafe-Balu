import { createStackNavigator } from '@react-navigation/stack'
import React from 'react'
import AllCategories from '../modules/categories/screens/AllCategories';

const Stack = createStackNavigator();

export default function CategoriesStack() {
  return (
    <Stack.Navigator>
        <Stack.Screen
            name='allCategoriesStack'
            component={AllCategories}
            options={{
                title: 'Categorías'
            }}
        />
    </Stack.Navigator>
  )
}