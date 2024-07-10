import { StyleSheet, Text, View } from "react-native";
import React from "react";
import { products } from "../functions/data";
import ContentCard from "../../../components/ContentCard";
import { ScrollView } from "react-native-gesture-handler";
import ViewProduct from "../../../components/ViewProduct";

var productsList = products;

export default function AllProducts() {
  return (
    <View style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>
        {productsList.map((product, index) => {
          return (
            <ViewProduct
              index={index}
              name={product.name}
              image={product.image}
              price={product.price}
              stock={product.stock}
              status={product.status}
              categoryName={product.category_name}
            />
          );
        })}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 10,
    backgroundColor: '#fff'
  },
});
