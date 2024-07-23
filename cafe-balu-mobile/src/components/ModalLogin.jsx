import {
  StyleSheet,
  View,
  KeyboardAvoidingView,
  Platform,
  Dimensions,
} from "react-native";
import React, { useState } from "react";
import { Overlay, Input, Button } from "@rneui/base";
import { isEmpty } from "lodash";
import { doPost } from "../config/axios";

const { height } = Dimensions.get("window");

export default function ModalLogin({ visible, setVisible, onLogin }) {
  const [errors, setErrors] = useState({ email: "", password: "" });
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [visiblePassword, setVisiblePassword] = useState(false);

  const login = async (username, password) => {
    try {
      const payload = {
        username: username,
        password: password,
      };

      const response = await doPost("/login", payload);
      if (response.data.id_token) //guardar en storage
      return true;
    } catch (error) {
      return false;
    }
  };

  const handleLogin = async () => {
    let valid = true;
    if (isEmpty(email)) {
      setErrors((prevErrors) => ({
        ...prevErrors,
        email: "El email es requerido",
      }));
      valid = false;
    }
    if (isEmpty(password)) {
      setErrors((prevErrors) => ({
        ...prevErrors,
        password: "La contraseña es requerida",
      }));
      valid = false;
    }
    if (valid) {
      const success = await login(email, password);

      if (success) {
        console.log("Inicio de sesión exitoso");
        closeModal();
      } else {
        console.log("Error en el inicio de sesión");
        setErrors((prevErrors) => ({
          ...prevErrors,
          general: "Error en el inicio de sesión",
        }));
      }
    }
  };

  const closeModal = () => {
    setVisible(false);
    setErrors({ email: "", password: "" });
    setEmail("");
    setPassword("");
  };

  return (
    <Overlay
      isVisible={visible}
      onBackdropPress={() => setVisible(!visible)}
      overlayStyle={styles.overlay}
      backdropStyle={styles.backdrop}
    >
      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        style={styles.keyboardAvoidingView}
      >
        <View>
          <Input
            label="Email"
            placeholder="ej: usuario@correo.com"
            labelStyle={styles.label}
            keyboardType="email-address"
            containerStyle={styles.inputContainer}
            autoCapitalize="none"
            onChange={(event) => setEmail(event.nativeEvent.text)}
            errorMessage={errors.email}
            rightIcon={{
              name: "account",
              type: "material-community",
              color: "#8B4513",
            }}
          />
          <Input
            label="Contraseña"
            placeholder="********"
            labelStyle={styles.label}
            secureTextEntry={!visiblePassword}
            containerStyle={styles.inputContainer}
            onChange={(event) => setPassword(event.nativeEvent.text)}
            errorMessage={errors.password}
            rightIcon={{
              name: visiblePassword ? "eye-off" : "eye",
              type: "material-community",
              color: "#8B4513",
              onPress: () => setVisiblePassword(!visiblePassword),
            }}
          />
          <View style={styles.row}>
            <Button
              title="Cancelar"
              buttonStyle={styles.closeButton}
              containerStyle={styles.buttonContainer}
              onPress={closeModal}
            />
            <Button
              title="Iniciar sesión"
              buttonStyle={styles.loginButton}
              containerStyle={styles.buttonContainer}
              onPress={handleLogin}
            />
          </View>
        </View>
      </KeyboardAvoidingView>
    </Overlay>
  );
}

const styles = StyleSheet.create({
  overlay: {
    width: "100%",
    height: height * 0.45,
    position: "absolute",
    bottom: 0,
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
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
  loginButton: {
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
  backdrop: {
    backgroundColor: "rgba(0, 0, 0, 0.5)",
  },
});
