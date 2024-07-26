import { StyleSheet, View, ScrollView, RefreshControl } from "react-native";
import React, { useEffect, useState, useCallback } from "react";
import ViewProducts from "../../../components/ViewProducts";
import { getAllProducts } from "../functions/functions";
import { SpeedDial } from "@rneui/themed";
import { useNavigation } from "@react-navigation/native";
import Loading from "../../../components/Loading";
import CustomToast from "../../../components/CustomToast";
import EmptyScreen from "../../../components/EmptyScreen";
import { tokenExists } from "../../../kernel/functions";

export default function AllProducts({ setReload, reload }) {
  const [products, setProducts] = useState([]);
  const [refreshing, setRefreshing] = useState(false);
  const [showLoading, setShowLoading] = useState(true);
  const [session, setSession] = useState(false);
  const [toastConfig, setToastConfig] = useState({
    visible: false,
    message: "",
    iconName: "",
    iconColor: "",
    toastColor: "",
  });

  const navigation = useNavigation();

  const checkSession = async () => {
    const session = await tokenExists();
    setSession(session);
  };

  useEffect(() => {
    const initialize = async () => {
      setShowLoading(true);
      await checkSession();
      await loadProducts();
      setShowLoading(false);
    };

    initialize();
  }, []);

  useEffect(() => {
    if (setReload) {
      loadProducts();
      setReload(false);
    }
  }, [reload]);

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
    checkSession();
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
          {products.length > 0 ? products.map((product, index) => (
            <ViewProducts
              id={product.id}
              key={index}
              index={index}
              name={product.name}
              image={product.image}
              price={product.price}
              stock={product.stock}
              status={product.status}
              description={product.description}
              categoryName={product.category_name}
            />
          )) : <EmptyScreen title={"Sin productos"} />}
        </ScrollView>
      )}
      {session && (
        <SpeedDial
          isOpen={false}
          icon={{ name: "add", color: "#fff" }}
          openIcon={{ name: "close", color: "#fff" }}
          buttonStyle={styles.buttonStyleDial}
          onOpen={() => navigation.navigate("newProductStack", { setReload })}
        >
          <SpeedDial.Action
            icon={{ name: "add", color: "#fff" }}
            title={"Nuevo producto"}
            onPress={() => console.log("do something")}
            buttonStyle={styles.buttonStyleDial}
          />
        </SpeedDial>
      )}
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