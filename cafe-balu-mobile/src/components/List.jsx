import { StyleSheet, Text, View } from "react-native";
import React, { useState } from "react";
import { Icon } from "@rneui/base";
import ModalChangeStatus from "./ModalChangeStatus";
import { TouchableOpacity } from "react-native-gesture-handler";

export default function List({ name, status, index, id, setReload }) {
  const [showModal, setShowModal] = useState(false);
  const [statusTag, setStatusTag] = useState(status)

  return (
    <View style={styles.categoryContainer} key={index}>
      <View style={styles.nameAndStatusContainer}>
        <Text style={styles.categoryName}>
          {name.length > 23 ? name.substring(0, 23) + "..." : name}
        </Text>
        <View
          style={[
            styles.status,
            statusTag === 1 ? styles.activeStatus : styles.inactiveStatus,
          ]}
        >
          <Text style={styles.statusText}>
            {statusTag === 1 ? "Activa" : "Inactiva"}
          </Text>
        </View>
      </View>
      <TouchableOpacity onPress={() => setShowModal(true)}>
        <Icon
          name={"dots-horizontal"}
          color={"#8B4513"}
          size={20}
          type="material-community"
        />
      </TouchableOpacity>
      <ModalChangeStatus
        type="CATEGORY"
        id={id}
        name={name}
        currentStatus={statusTag}
        setStatusTag={setStatusTag}
        visible={showModal}
        setVisible={setShowModal}
        setReload={setReload}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  categoryContainer: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    padding: 16,
    backgroundColor: "#fff",
    marginBottom: 16,
    borderRadius: 8,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 2,
  },
  nameAndStatusContainer: {
    flexDirection: "row",
    alignItems: "center",
    flex: 1,
  },
  categoryName: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#8B4513",
    marginRight: 10,
  },
  status: {
    paddingVertical: 4,
    paddingHorizontal: 8,
    borderRadius: 4,
    justifyContent: 'center',
    alignItems: 'center',
  },
  activeStatus: {
    backgroundColor: "#DFF0D8",
  },
  inactiveStatus: {
    backgroundColor: "#F2DEDE",
  },
  statusText: {
    color: "#333",
    fontSize: 14,
  },
});
