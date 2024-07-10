import { StyleSheet, Text, View } from "react-native";
import React, { useEffect, useState } from "react";
import ContentCard from "../../../components/ContentCard";
import { ScrollView } from "react-native-gesture-handler";
import ViewProducts from "../../../components/ViewProducts";
import { getAllProducts } from "../functions/functions";

export default function AllProducts() {
  const [reloadComponent, setReloadComponent] = useState(false)
  const [products, setProducts] = useState([]);

  useEffect(async () => {
    let productList = await getAllProducts()
    setProducts(productList);
  },[reloadComponent])
  

  return (
    <View style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>
        {products.map((product, index) => {
          return (
            <ViewProducts
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
    backgroundColor: "#fff",
  },
});
