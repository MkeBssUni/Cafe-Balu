import { createStackNavigator } from '@react-navigation/stack'
import React from 'react'
import AllProducts from '../modules/products/screens/AllProducts'

const Stack = createStackNavigator();

export default function ProductsStack() {
  return (
    <Stack.Navigator>
        <Stack.Screen
            name='allProductsStack'
            component={AllProducts}
            options={{
                title: 'Productos'
            }}
        />
    </Stack.Navigator>
  )
}