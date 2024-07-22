import React from "react";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { NavigationContainer } from "@react-navigation/native";
import ProductsStack from "../stack/ProductsStack";
import CategoriesStack from "../stack/CategoriesStack";
import { Icon } from "@rneui/base";
import SalesStack from "../stack/SalesStack";

const Tab = createBottomTabNavigator();

export default function Navigation({setReload}) {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={({ route }) => ({
          tabBarIcon: ({ color }) => screenOptions(route, color),
          tabBarActiveTintColor: "#8B4513",
          tabBarInactiveTintColor: "#A77B4A",
          headerShown: false,
          tabBarStyle: {
            backgroundColor: "#F5F5F5",
            borderTopColor: "#A77B4A",
            borderTopWidth: 1
          },
        })}
        initialRouteName="sales"
      >
        <Tab.Screen
          name="sales"
          component={SalesStack}
          options={{
            title: "Ventas",
          }}
        />
        <Tab.Screen
          name="products"
          component={ProductsStack}
          options={{
            title: "Productos",
          }}
          initialParams={{setReload}}
        />
        <Tab.Screen
          name="categories"
          component={CategoriesStack}
          options={{
            title: "Categorias",
          }}
        />
      </Tab.Navigator>
    </NavigationContainer>
  );
}

const screenOptions = (route, color) => {
  let iconName;
  switch (route.name) {
    case "sales":
      iconName = "currency-usd";
      break;
    case "products":
      iconName = "food-fork-drink";
      break;
    case "categories":
      iconName = "tag-multiple";
      break;
  }
  return (
    <Icon type="material-community" name={iconName} size={22} color={color} />
  );
};
