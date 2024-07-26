import {
  StyleSheet,
  Text,
  View,
  Modal,
  Animated,
  Dimensions,
  TouchableWithoutFeedback,
} from "react-native";
import React, { useState, useRef, useEffect } from "react";
import { Divider, ListItem } from "@rneui/themed";
import { Switch } from "@rneui/themed";
import CustomToast from "./CustomToast";
import { changeStatusCategoryOrProduct } from "../kernel/functions";

const { height } = Dimensions.get("window");

export default function ModalChangeStatus({
  id,
  name,
  type,
  visible,
  setVisible,
  setReload,
  currentStatus,
  setStatusTag,
}) {
  const [checked, setChecked] = useState(currentStatus == 1);
  const [toastConfig, setToastConfig] = useState({
    visible: false,
    message: "",
    iconName: "",
    iconColor: "",
    toastColor: "",
  });

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

  const toggleSwitch = async (value) => {
    setChecked(value);
    const status = value ? 1 : 0;
    const response = await changeStatusCategoryOrProduct(id, type, status);
    if (response.success) {
      setStatusTag(status);
      showToast(response.message, "check-circle", "#fff", "#00B82C");
    } else {
      showToast(response.message, "alert-circle", "#fff", "#FF0000");
    }
  };

  const showToast = (message, iconName, iconColor, toastColor) => {
    setToastConfig({ visible: true, message, iconName, iconColor, toastColor });
  };

  const handleHideToast = () => {
    setToastConfig((prevState) => ({ ...prevState, visible: false }));
  };

  const closeModal = (needsReload) => {
    Animated.timing(translateY, {
      toValue: height,
      duration: 400,
      useNativeDriver: true,
    }).start(() => {
      setVisible(false);
      if (needsReload) {
        setReload(true);
      }
    });
  };

  return (
    <Modal transparent animationType="none" visible={visible}>
      <TouchableWithoutFeedback onPress={() => closeModal()}>
        <View style={styles.backdrop} />
      </TouchableWithoutFeedback>
      <Animated.View style={[styles.animatedOverlay, { transform: [{ translateY }] }]}>
        <View>
          <Text style={styles.modalTitle}>Acciones para {name}</Text>
        </View>
        <Divider style={styles.divider} />
        <ListItem>
          <ListItem.Content>
            <View style={styles.row}>
              <ListItem.Title>Cambiar estado</ListItem.Title>
              <Switch
                value={checked}
                onValueChange={(value) => toggleSwitch(value)}
                color="#8B4513"
                style={styles.switch}
              />
            </View>
          </ListItem.Content>
        </ListItem>
        <Divider style={styles.divider} />
        <CustomToast {...toastConfig} onHide={handleHideToast} />
      </Animated.View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  backdrop: {
    flex: 1,
    backgroundColor: "rgba(0, 0, 0, 0.5)",
  },
  animatedOverlay: {
    position: "absolute",
    bottom: 0,
    width: "100%",
    backgroundColor: "white",
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    padding: 20,
    height: height * 0.24,
  },
  modalTitle: {
    fontSize: 20,
    fontWeight: "bold",
    marginBottom: 5,
  },
  divider: {
    borderWidth: 0.5,
    marginVertical: 8,
  },
  row: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  switch: {
    marginLeft: 180,
  },
  centerLoadingContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
});
