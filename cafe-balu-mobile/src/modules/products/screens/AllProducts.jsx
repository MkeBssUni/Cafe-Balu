import { StyleSheet, View, ScrollView, RefreshControl } from "react-native";
import React, { useEffect, useState, useCallback } from "react";
import ViewProducts from "../../../components/ViewProducts";
import { getAllProducts } from "../functions/functions";
import { SpeedDial } from "@rneui/themed";
import { useNavigation } from "@react-navigation/native";
import Loading from "../../../components/Loading";

export default function AllProducts() {
  const [products, setProducts] = useState([]);
  const [refreshing, setRefreshing] = useState(false);
  const [showLoading, setShowLoading] = useState(true);
  const navigate = useNavigation();

  const loadProducts = async () => {
    try {
      const productList = await getAllProducts();
      setProducts(productList.reverse());
    } catch (error) {
      console.error("Error fetching products: ", error);
    }
  };

  useEffect(() => {
    setShowLoading(true);
    loadProducts();
    setShowLoading(false);
  }, []);
  
  const onRefresh = useCallback(() => {
    setRefreshing(true);
    loadProducts().then(() => {
      setRefreshing(false);
    });
  }, []);

  return !showLoading ? (
    <View style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollViewContent}
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh}/>
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
      <SpeedDial
        isOpen={false}
        icon={{
          name: "add",
          color: "#fff",
        }}
        openIcon={{
          name: "close",
          color: "#fff",
        }}
        buttonStyle={styles.buttonStyleDial}
        onOpen={() => navigate.navigate("newProductStack")}
      >
        <SpeedDial.Action
          icon={{
            name: "add",
            color: "#fff",
          }}
          title={"Nuevo producto"}
          onPress={() => console.log("do something")}
          buttonStyle={styles.buttonStyleDial}
        />
      </SpeedDial>
    </View>
  ) : (
    <Loading />
  )
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
  buttonStyleDial: {
    backgroundColor: "#A77B4A",
  },
});
