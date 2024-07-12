import {
  StyleSheet,
  View,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import React, { useState } from "react";
import { Overlay, Input, Button } from "@rneui/base";
import { isEmpty } from "lodash";
import { newCategory } from "../modules/categories/functions/functions";

export default function ModalNewCateogry({ openDial, setOpenDial, onRefresh}) {
  const [errors, setErrors] = useState({ name: "" });
  const [categoryName, setCategoryName] = useState("");

  const sendData = () =>{
    console.log(categoryName)
    if (isEmpty(categoryName)) {
      setErrors({ name: "El nombre es requerido" });
      return;
    }

    if(!categoryName.length >= 3 && !categoryName.length <= 50){
      setErrors({ name: "El nombre debe tener entre 3 y 50 caracteres" });
      return;
    }

    var success = newCategory(categoryName);

    if(success){
      console.log("Categoria guardada con exito");
      closeModal();
      onRefresh();
    }else{
      console.log("Error al guardar la categoria");
    }

  }

  const closeModal = () => {
    setOpenDial(false);
    setErrors({ name: "" });
    setCategoryName("");
  };

  return (
    <Overlay
      isVisible={openDial}
      onBackdropPress={() => setOpenDial(!openDial)}
      overlayStyle={styles.overlay}
    >
      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        style={styles.keyboardAvoidingView}
      >
        <View>
          <Input
            label="Nombre de la categoria"
            placeholder="ej: Bebidas"
            labelStyle={styles.label}
            keyboardType="default"
            containerStyle={styles.inputContainer}
            autoCapitalize="sentences"
            onChange={(event) => setCategoryName(event.nativeEvent.text)}
            errorMessage={errors.name}
          />
          <View style={styles.row}>
            <Button
              title="Cerrar"
              buttonStyle={styles.closeButton}
              containerStyle={styles.buttonContainer}
              onPress={closeModal}
            />

            <Button
              title="Guardar"
              buttonStyle={styles.saveButton}
              containerStyle={styles.buttonContainer}
              onPress={() => {
                sendData();
              }}
            />
          </View>
        </View>
      </KeyboardAvoidingView>
    </Overlay>
  );
}

const styles = StyleSheet.create({
  overlay: {
    borderRadius: 20,
    width: "80%",
    padding: 20,
    backgroundColor: "white",
  },
  keyboardAvoidingView: {
    width: "100%",
  },
  label: {
    color: "#8B4513",
    fontSize: 16,
    marginBottom: 10,
  },
  inputContainer: {
    marginBottom: 20,
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
    width: "40%",
    alignSelf: "center",
  },
  row: {
    flexDirection: "row",
    justifyContent: "space-between",
  },
});
