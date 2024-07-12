import { createStackNavigator } from '@react-navigation/stack'
import React from 'react'
import AllProducts from '../modules/products/screens/AllProducts'
import NewProduct from '../modules/products/screens/NewProduct';

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
        <Stack.Screen
            name='newProductStack'
            component={NewProduct}
            options={{
                title: 'Registrar producto'
            }}
        />
    </Stack.Navigator>
  )
}