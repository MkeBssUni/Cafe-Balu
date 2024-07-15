import { View, Text } from "react-native";
import React from "react";
import { createStackNavigator } from "@react-navigation/stack";
import AllSales from "../modules/sales/screens/AllSales";

const Stack = createStackNavigator();

export default function SalesStack() {
  return (
    <Stack.Navigator>
      <Stack.Screen
        name="allSalesStack"
        component={AllSales}
        options={{
          title: "Historial de ventas",
        }}
      />
    </Stack.Navigator>
  );
}
