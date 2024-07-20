import { StyleSheet, View, ScrollView, RefreshControl } from "react-native";
import React, { useEffect, useState, useCallback } from "react";
import ViewProducts from "../../../components/ViewProducts";
import { getAllProducts } from "../functions/functions";
import { SpeedDial } from "@rneui/themed";
import { useNavigation } from "@react-navigation/native";
import Loading from "../../../components/Loading";
import CustomToast from "../../../components/CustomToast";

export default function AllProducts() {
  const [products, setProducts] = useState([]);
  const [refreshing, setRefreshing] = useState(false);
  const [showLoading, setShowLoading] = useState(true);
  const [toastConfig, setToastConfig] = useState({
    visible: false,
    message: "",
    iconName: "",
    iconColor: "",
    toastColor: "",
  });

  const navigation = useNavigation();

  
  useEffect(() => {
    setShowLoading(true);
    loadProducts();
  }, []);
  
  const showToast = (message, iconName, iconColor, toastColor) => {
    setToastConfig({ visible: true, message, iconName, iconColor, toastColor });
  };

  const handleHideToast = () => {
    setToastConfig((prevState) => ({ ...prevState, visible: false }));
  };

  const loadProducts = async () => {
    try {
      const productList = await getAllProducts();
      setProducts(productList.reverse());
    } catch (error) {
      showToast("Error al cargar los productos", "alert-circle", "#fff", "#FF3232");
    } finally {
      setShowLoading(false);
    }
  };
  
  const onRefresh = useCallback(() => {
    setRefreshing(true);
    loadProducts().then(() => {
      setRefreshing(false);
    });
  }, []);

  return (
    <View style={styles.container}>
      {showLoading ? (
        <Loading />
      ) : (
        <ScrollView
          style={styles.scrollView}
          contentContainerStyle={styles.scrollViewContent}
          showsVerticalScrollIndicator={false}
          refreshControl={
            <RefreshControl
              refreshing={refreshing}
              onRefresh={onRefresh}
              colors={["#8B4513"]}
            />
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
      )}
      <SpeedDial
        isOpen={false}
        icon={{ name: "add", color: "#fff" }}
        openIcon={{ name: "close", color: "#fff" }}
        buttonStyle={styles.buttonStyleDial}
        onOpen={() => navigation.navigate("newProductStack")}
      >
        <SpeedDial.Action
          icon={{ name: "add", color: "#fff" }}
          title={"Nuevo producto"}
          onPress={() => console.log("do something")}
          buttonStyle={styles.buttonStyleDial}
        />
      </SpeedDial>
      <CustomToast {...toastConfig} onHide={handleHideToast} />
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
  buttonStyleDial: {
    backgroundColor: "#A77B4A",
  },
});
