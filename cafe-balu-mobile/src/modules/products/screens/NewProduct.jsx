import { StyleSheet, Image, View, ScrollView } from "react-native";
import React, { useState, useEffect } from "react";
import { Button, Input } from "@rneui/base";
import * as ImagePicker from "expo-image-picker";
import { isEmpty } from "lodash";
import { saveProduct } from "../functions/functions";
import { useNavigation, useRoute } from "@react-navigation/native";
import Select from "../../../components/Select";
import { getAllCategories } from "../../categories/functions/functions";
import CustomToast from "../../../components/CustomToast";

export default function NewProduct() {
  const [categories, setCategories] = useState([]);
  const [toastConfig, setToastConfig] = useState({
    visible: false,
    message: "",
    iconName: "",
    iconColor: "",
    toastColor: "",
  });
  const route = useRoute();
  const navigation = useNavigation();

  const [errors, setErrors] = useState({
    name: "",
    stock: "",
    price: "",
    category: "",
    image: "",
  });
  const [newProduct, setNewProduct] = useState({
    name: "",
    stock: "",
    price: "",
    category_id: category,
    image: null,
  });
  const [image, setImage] = useState(null);
  const [category, setCategory] = useState(0);

  const showToast = (message, iconName, iconColor, toastColor) => {
    setToastConfig({ visible: true, message, iconName, iconColor, toastColor });
  };

  const handleHideToast = () => {
    setToastConfig((prevState) => ({ ...prevState, visible: false }));
  };

  useEffect(() => {
    const fetchCategories = async () => {
      const categoriesData = await getAllCategories();
      setCategories(categoriesData);
    };
    fetchCategories();
  }, []);

  const handleChange = (name, value) => {
    setNewProduct({
      ...newProduct,
      [name]: value,
    });
  };

  const pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 4],
      quality: 1,
      base64: true,
    });
    if (!result.canceled) {
      const { uri, base64 } = result.assets[0];
      const imageFormat = uri.split(".").pop();
      const base64Image = `data:image/${imageFormat};base64,${base64}`;
      setImage(uri);
      handleChange("image", base64Image);
    }
  };

  const cleanForm = () => {
    setNewProduct({
      name: "",
      stock: "",
      price: "",
      category_id: 1,
      image: null,
    });
    setImage(null);
    setErrors({
      name: "",
      stock: "",
      price: "",
      category: "",
      image: "",
    });
  };

  const sendData = () => {
    setErrors({ name: "", stock: "", price: "", category: "", image: "" });

    const updatedProduct = {
      ...newProduct,
      stock: parseInt(newProduct.stock),
      price: parseFloat(newProduct.price),
      category_id: category,
    };

    if (isEmpty(updatedProduct.name)) {
      setErrors((prev) => ({ ...prev, name: "El nombre es requerido" }));
      return;
    }
    if (isNaN(updatedProduct.stock)) {
      setErrors((prev) => ({ ...prev, stock: "El stock es requerido" }));
      return;
    }
    if (isNaN(updatedProduct.price)) {
      setErrors((prev) => ({ ...prev, price: "El precio es requerido" }));
      return;
    }

    if (updatedProduct.stock <= 0) {
      setErrors((prev) => ({ ...prev, stock: "El stock debe ser mayor a 0" }));
      return;
    }

    if (updatedProduct.price <= 0) {
      setErrors((prev) => ({ ...prev, price: "El precio debe ser mayor a 0" }));
      return;
    }
    
    if(updatedProduct.category_id === 0 || updatedProduct.category_id === undefined){
      showToast("La categoría es requerida", "alert-circle", "#fff", "#FF0000");
      return;
    }

    if (isEmpty(updatedProduct.image)) {
      showToast("La imagen es requerida", "alert-circle", "#fff", "#FF0000");
      return;
    }

    const result = saveProduct(updatedProduct);
    if (result) {
      showToast("Producto guardado", "check-circle", "#fff", "#00B82C");
      setTimeout(() => {
        cleanForm();
        navigation.navigate("allProductsStack");
      }, 2000);
    }
  };

  return (
    <View style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        showsVerticalScrollIndicator={false}
      >
        <Input
          label="Nombre del producto"
          placeholder="ej: Muffin de chocolate"
          labelStyle={styles.label}
          keyboardType="default"
          containerStyle={styles.inputContainer}
          autoCapitalize="sentences"
          onChange={(event) => handleChange("name", event.nativeEvent.text)}
          errorMessage={errors.name}
          value={newProduct.name}
        />
        <View style={styles.row}>
          <Input
            label="Stock"
            placeholder="ej: 10"
            labelStyle={styles.label}
            keyboardType="numeric"
            containerStyle={styles.inputContainerRow}
            onChange={(event) => handleChange("stock", event.nativeEvent.text)}
            errorMessage={errors.stock}
            value={newProduct.stock}
          />
          <Input
            label="Precio"
            placeholder="ej: 25.00"
            labelStyle={styles.label}
            keyboardType="numeric"
            containerStyle={styles.inputContainerRow}
            onChange={(event) => handleChange("price", event.nativeEvent.text)}
            errorMessage={errors.price}
            value={newProduct.price}
          />
        </View>
        <Select
          value={category}
          setValue={setCategory}
          label={"Selecciona una categoría"}
          list={categories}
          defaultTitle={"Categoría"}
        />
        <Button
          title={image ? "Cambiar imagen" : "Seleccionar imagen"}
          onPress={pickImage}
          buttonStyle={styles.imgPickerButton}
          iconRight={true}
          icon={
            image
              ? {
                  name: "image-edit",
                  type: "material-community",
                  size: 22,
                  color: "white",
                }
              : {
                  name: "image-plus",
                  type: "material-community",
                  size: 22,
                  color: "white",
                }
          }
        />
        {image && <Image source={{ uri: image }} style={styles.image} />}
        <View style={styles.row}>
          <Button
            title="Limpiar"
            buttonStyle={styles.closeButton}
            containerStyle={styles.buttonContainer}
            onPress={cleanForm}
          />

          <Button
            title="Guardar"
            buttonStyle={styles.saveButton}
            containerStyle={styles.buttonContainer}
            onPress={sendData}
          />
        </View>
      </ScrollView>
      <CustomToast {...toastConfig} onHide={handleHideToast} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    padding: 15,
  },
  scrollView: {
    flex: 1,
  },
  label: {
    color: "#8B4513",
    fontSize: 16,
    marginBottom: 10,
  },
  inputContainer: {
    marginBottom: 20,
  },
  inputContainerRow: {
    marginBottom: 20,
    flex: 1,
  },
  row: {
    flexDirection: "row",
    justifyContent: "space-between",
  },
  image: {
    width: 280,
    height: 280,
    marginTop: 20,
    alignSelf: "center",
  },
  imgPickerButton: {
    backgroundColor: "#D2B48C",
    borderRadius: 10,
    marginTop: 20,
  },
  saveButton: {
    backgroundColor: "#A77B4A",
    borderRadius: 10,
  },
  closeButton: {
    backgroundColor: "#9e9e9e",
    borderRadius: 10,
  },
  buttonContainer: {
    marginTop: 20,
    width: "40%",
    alignSelf: "center",
  },
});
