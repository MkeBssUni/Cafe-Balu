import { StyleSheet, Text, View } from "react-native";
import React, { useState } from "react";
import { Image, Card } from "@rneui/themed";
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
          <View style={[styles.row,{
            justifyContent: "space-between",
            alignItems: "center",
          }]}> 
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
          <Card.Divider style={styles.carDivider} />
          <View style={styles.row}>
            <Text style={styles.rowItem}>${price}</Text>
            <Text style={styles.rowItem}>Stock: {stock}</Text>
          </View>
          <View style={styles.row}>
            <View
              style={[
                styles.status,
                statusTag === 1 ? styles.activeStatus : styles.inactiveStatus,
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
    flex: 1,
    flexDirection: "row",
  },
  rowItem: {
    flex: 1,
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
    marginBottom: 16,
  },
  dataContainer: {
    flex: 1,
    paddingLeft: 8,
  },
  carDivider: {
    borderWidth: 0.5,
  },
  status: {
    padding: 4,
    borderRadius: 4,
    height: 30,
    marginTop: 8,
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
