import { StyleSheet, View, ScrollView, RefreshControl } from "react-native";
import React, { useEffect, useState, useCallback } from "react";
import ViewProducts from "../../../components/ViewProducts";
import { getAllProducts } from "../functions/functions";

export default function AllProducts() {
  const [products, setProducts] = useState([]);
  const [refreshing, setRefreshing] = useState(false);

  const loadProducts = async () => {
    try {
      const productList = await getAllProducts();
      setProducts(productList);
    } catch (error) {
      console.error("Error fetching products: ", error);
    }
  };

  useEffect(() => {
    loadProducts();
  }, []);

  const onRefresh = useCallback(() => {
    setRefreshing(true);
    loadProducts().then(() => {
      setRefreshing(false);
    });
  }, []);

  return (
    <View style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollViewContent}
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {products.map((product, index) => (
          <ViewProducts
            key={index}
            index={index}
            name={product.name}
            image={product.image}
            price={product.price}
            stock={product.stock}
            status={product.status}
            categoryName={product.category_name}
          />
        ))}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
  },
  scrollView: {
    flex: 1,
  },
  scrollViewContent: {
    padding: 10,
  },
});