import React from "react";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { NavigationContainer } from "@react-navigation/native";
import ProductsStack from "../stack/ProductsStack";
import CategoriesStack from "../stack/CategoriesStack";
import { Icon } from "@rneui/base";

const Tab = createBottomTabNavigator();

export default function Navigation() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={({ route }) => ({
          tabBarIcon: ({ color }) => screenOptions(route, color),
          tabBarActiveTintColor: "#8B4513",
          tabBarInactiveTintColor: "#D2B48C",
          headerShown: false,
          tabBarStyle: {
            backgroundColor: "#F5F5F5",
            borderTopColor: "#D2B48C",
            borderTopWidth: 1
          },
        })}
        initialRouteName="products"
      >
        <Tab.Screen
          name="products"
          component={ProductsStack}
          options={{
            title: "Productos",
          }}
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
