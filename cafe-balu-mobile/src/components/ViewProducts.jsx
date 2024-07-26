import { StyleSheet, Text, View } from "react-native";
import React, { useState } from "react";
import { Image, Card, Divider } from "@rneui/themed";
import { cafeBase64 } from "../assets/imgs/imgs-base64";
import ModalChangeStatus from "./ModalChangeStatus";
import { Icon } from "@rneui/base";
import { TouchableOpacity } from "react-native-gesture-handler";

export default function ViewProducts({
  id,
  name,
  image,
  price,
  index,
  stock,
  status,
  description,
}) {
  const [showModal, setShowModal] = useState(false);
  const [statusTag, setStatusTag] = useState(status);
  return (
    <Card containerStyle={styles.card}>
      <View key={index} style={styles.rowContainer}>
        <View style={styles.imgContainer}>
          <Image
            resizeMode="contain"
            style={styles.img}
            source={{
              uri: image || cafeBase64,
            }}
          />
        </View>
        <View style={styles.dataContainer}>
          <View
            style={[
              styles.row,
              {
                justifyContent: "space-between",
                alignItems: "center",
              },
            ]}
          >
            <Text style={styles.title}>{name}</Text>
            <TouchableOpacity onPress={() => setShowModal(true)}>
              <Icon
                name={"dots-horizontal"}
                color={"#8B4513"}
                size={20}
                type="material-community"
              />
            </TouchableOpacity>
          </View>
          <Card.Divider style={styles.cardDivider} />
          <Text style={styles.description}>{description || 'Sin descripción disponible'}</Text>
          <Card.Divider style={styles.cardDivider} />
          <View style={[styles.row, styles.distributedRow]}>
            <Text style={styles.rowItem}>${price}</Text>
            <Divider orientation="vertical" />
            <View style={styles.rowItem}>
              <Text style={styles.rowItem}>Stock:</Text>
              <Text style={styles.rowItem}>{stock}</Text>
            </View>
            <Divider orientation="vertical" />
            <View
              style={[
                styles.status,
                statusTag === 1 ? styles.activeStatus : styles.inactiveStatus,
                styles.rowItem
              ]}
            >
              <Text style={styles.statusText}>
                {statusTag === 1 ? "Activo" : "Inactivo"}
              </Text>
            </View>
          </View>
        </View>
      </View>
      <ModalChangeStatus
        type="PRODUCT"
        id={id}
        name={name}
        currentStatus={statusTag}
        setStatusTag={setStatusTag}
        visible={showModal}
        setVisible={setShowModal}
      />
    </Card>
  );
}

const styles = StyleSheet.create({
  rowContainer: {
    flex: 1,
    flexDirection: "row",
    paddingBottom: 8,
  },
  card: {
    borderRadius: 12,
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 5,
    },
    shadowOpacity: 0.34,
    shadowRadius: 6.27,
    elevation: 2,
  },
  row: {
    flexDirection: "row",
  },
  distributedRow: {
    justifyContent: "space-between",
    alignItems: "center",
  },
  rowItem: {
    flex: 1,
    textAlign: "center",
  },
  imgContainer: {
    position: "relative",
    alignItems: "center",
  },
  img: {
    width: 128,
    height: 128,
  },
  title: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#8B4513",
  },
  dataContainer: {
    flex: 1,
    paddingLeft: 8,
  },
  cardDivider: {
    borderWidth: 0.5,
    marginVertical: 8,
  },
  description: {
    fontSize: 14,
    color: "#666",
    marginBottom: 8,
  },
  status: {
    padding: 4,
    borderRadius: 4,
    height: 30,
    marginTop: 8,
    marginHorizontal: 4,
    justifyContent: "center",
    alignItems: "center",
  },
  activeStatus: {
    backgroundColor: "#DFF0D8",
  },
  inactiveStatus: {
    backgroundColor: "#F2DEDE",
  },
  statusText: {
    fontSize: 14,
    color: "#000",
  },
});
