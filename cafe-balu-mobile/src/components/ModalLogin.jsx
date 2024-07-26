import React, { useState, useEffect, useRef } from "react";
import {
  StyleSheet,
  View,
  KeyboardAvoidingView,
  Platform,
  Dimensions,
  Animated,
  Modal,
  TouchableWithoutFeedback,
} from "react-native";
import { Input, Button } from "@rneui/base";
import { isEmpty } from "lodash";
import { doPost } from "../config/axios";
import AsyncStorage from "@react-native-async-storage/async-storage";
import CustomToast from "./CustomToast";
import Loading from "./Loading";

const { height } = Dimensions.get("window");

export default function ModalLogin({ visible, setVisible, setReload }) {
  const [errors, setErrors] = useState({ email: "", password: "" });
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [visiblePassword, setVisiblePassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const [toastConfig, setToastConfig] = useState({
    visible: false,
    message: "",
    iconName: "",
    iconColor: "",
    toastColor: "",
  });

  const showToast = (message, iconName, iconColor, toastColor) => {
    setToastConfig({ visible: true, message, iconName, iconColor, toastColor });
  };

  const handleHideToast = () => {
    setToastConfig((prevState) => ({ ...prevState, visible: false }));
  };

  const translateY = useRef(new Animated.Value(height)).current;

  useEffect(() => {
    if (visible) {
      Animated.timing(translateY, {
        toValue: 0,
        duration: 400,
        useNativeDriver: true,
      }).start();
    }
  }, [visible]);

  const login = async (username, password) => {
    try {
      const payload = {
        username: username,
        password: password,
      };

      const response = await doPost("/login", payload);
      
      if(response.data.role !== "admin") {
        showToast("No tienes permisos para acceder", "alert-circle", "#fff", "#FF0000");
        return { success: false, message: "No tienes permisos para acceder" };
      }
      if (response.data.id_token) await AsyncStorage.setItem("token", response.data.id_token);
      return { success: true, message: "Inicio de sesión exitoso" };
    } catch (error) {
      return { success: false, message: "No se pudo iniciar sesión"}
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
      setLoading(true);
      const response = await login(email, password);
      setLoading(false);

      if (response.success) {
        showToast(response.message, "check-circle", "#fff", "#00B82C");
        closeModal();
      } else {
        showToast(response.message, "alert-circle", "#fff", "#FF0000");
      }
    }
  };

  const closeModal = () => {
    Animated.timing(translateY, {
      toValue: height,
      duration: 400,
      useNativeDriver: true,
    }).start(() => {
      setVisible(false);
      setReload(true);
      setErrors({ email: "", password: "" });
      setEmail("");
      setPassword("");
    });
  };

  return (
    <Modal
      transparent
      animationType="none"
      visible={visible}
      onRequestClose={closeModal}
    >
      <TouchableWithoutFeedback onPress={closeModal}>
        <View style={styles.backdrop} />
      </TouchableWithoutFeedback>
      <Animated.View style={[styles.animatedOverlay, { transform: [{ translateY }] }]}>
        {loading ? (
          <Loading />
        ) : (
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
        )}
        <CustomToast {...toastConfig} onHide={handleHideToast} />
      </Animated.View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  animatedOverlay: {
    position: 'absolute',
    bottom: 0,
    width: '100%',
    backgroundColor: 'white',
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    padding: 20,
    height: height * 0.45,
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
    flex: 1,
    backgroundColor: "rgba(0, 0, 0, 0.5)",
  },
});

