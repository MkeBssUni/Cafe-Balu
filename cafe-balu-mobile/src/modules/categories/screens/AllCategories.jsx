import { ScrollView, StyleSheet, View, RefreshControl } from "react-native";
import React, { useState, useEffect, useCallback } from "react";
import { categoriesList } from "../../../kernel/data";
import List from "../../../components/List";
import { getAllCategories } from "../functions/functions";
import { SpeedDial } from "@rneui/themed";
import ModalNewCateogry from "../../../components/ModalNewCateogry";

export default function AllCategories() {
  const [categories, setCategories] = useState(categoriesList);
  const [refreshing, setRefreshing] = useState(false);
  const [openDial, setOpenDial] = useState(false);

  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () => {
    try {
      const categoriesList = await getAllCategories();
      setCategories(categoriesList);
    } catch (error) {
      console.log("error categories: ", error);
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
      <ScrollView
        style={styles.scrollView}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scrollViewContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {categories.map((category, index) => (
          <List index={index} name={category.name} status={category.status} />
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
      <ModalNewCateogry openDial={openDial} setOpenDial={setOpenDial} onRefresh={onRefresh} />
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
