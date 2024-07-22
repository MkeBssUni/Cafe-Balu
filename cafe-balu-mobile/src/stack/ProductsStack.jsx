import { createStackNavigator } from '@react-navigation/stack'
import React, { useState } from 'react'
import AllProducts from '../modules/products/screens/AllProducts'
import NewProduct from '../modules/products/screens/NewProduct';

const Stack = createStackNavigator();

export default function ProductsStack() {
  const [reload, setReload] = useState(false);

  return (
    <Stack.Navigator>
        <Stack.Screen
            name='allProductsStack'
            options={{
                title: 'Productos'
            }}
        >
          {props => <AllProducts {...props} setReload={setReload} reload={reload} />}
        </Stack.Screen>
        <Stack.Screen
            name='newProductStack'
            options={{
                title: 'Registrar producto'
            }}
        >
          {props => <NewProduct {...props} setReload={setReload} />}
        </Stack.Screen>
    </Stack.Navigator>
  )
}
