import { ScrollView, StyleSheet, View, RefreshControl } from "react-native";
import React, { useState, useEffect, useCallback } from "react";
import List from "../../../components/List";
import { getAllCategories } from "../functions/functions";
import { SpeedDial } from "@rneui/themed";
import ModalNewCateogry from "../../../components/ModalNewCateogry";
import Loading from "../../../components/Loading";
import CustomToast from "../../../components/CustomToast";
import EmptyScreen from "../../../components/EmptyScreen";

export default function AllCategories() {
  const [categories, setCategories] = useState([]);
  const [refreshing, setRefreshing] = useState(false);
  const [openDial, setOpenDial] = useState(false);

  const [showLoading, setShowLoading] = useState(true);
  const [toastConfig, setToastConfig] = useState({
    visible: false,
    message: "",
    iconName: "",
    iconColor: "",
    toastColor: "",
  });

  useEffect(() => {
    loadCategories();
  }, []);

  const showToast = (message, iconName, iconColor, toastColor) => {
    setToastConfig({ visible: true, message, iconName, iconColor, toastColor });
  };

  const handleHideToast = () => {
    setToastConfig((prevState) => ({ ...prevState, visible: false }));
  };

  const loadCategories = async () => {
    try {
      const categoriesList = await getAllCategories(0);
      setCategories(categoriesList.reverse());
    } catch (error) {
      showToast(
        "Error al cargar las categorías",
        "alert-circle",
        "#fff",
        "#FF3232"
      );
    } finally {
      setShowLoading(false);
    }
  };

  const onRefresh = useCallback(() => {
    setRefreshing(true);
    loadCategories().then(() => {
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
          showsVerticalScrollIndicator={false}
          contentContainerStyle={styles.scrollViewContent}
          refreshControl={
            <RefreshControl
              refreshing={refreshing}
              onRefresh={onRefresh}
              colors={["#8B4513"]}
            />
          }
        >
          {
            categories.length > 0 ?
              categories.map((category, index) => (
                <List index={index} name={category.name} status={category.status} />
              ))
            : <EmptyScreen title={"Sin categorías"} />
          }
        </ScrollView>
      )}
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
        onOpen={() => setOpenDial(!openDial)}
        onClose={() => setOpenDial(!openDial)}
        buttonStyle={styles.buttonStyleDial}
      >
        <SpeedDial.Action
          icon={{
            name: "add",
            color: "#fff",
          }}
          title={"Nueva categoría"}
          onPress={() => console.log("do something")}
          buttonStyle={styles.buttonStyleDial}
        />
      </SpeedDial>
      <ModalNewCateogry
        openDial={openDial}
        setOpenDial={setOpenDial}
        onRefresh={onRefresh}
      />
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
