import { StyleSheet, Text, View } from "react-native";
import React from "react";
import { Card, Image } from "@rneui/themed";
import { cafeBase64 } from "../assets/imgs/imgs-base64";

export default function ContentCard(props) {
  const { id, name, image, price, index } = props;

  return (
    <Card key={index}>
      <View style={styles.row}>
        <Card.Title style={styles.cardText}>{name}</Card.Title>
        <Card.Title style={styles.cardText}>${price}</Card.Title>
      </View>
      <Card.Divider style={styles.cardDivider} />
      <View style={styles.imgContainer}>
        <Image
          resizeMode="contain"
          style={styles.img}
          source={{
            uri: cafeBase64,
          }}
        />
      </View>
    </Card>
  );
}

const styles = StyleSheet.create({
  cardDivider: {
    backgroundColor: "#DAA520",
  },
  cardText: {
    color: "#8B4513",
    flex: 1,
  },
  imgContainer: {
    position: "relative",
    alignItems: "center",
  },
  img: {
    /* width:"100%",
        height:100 */
    width: 128,
    height: 128,
  },
  row: {
    flex: 1,
    flexDirection: "row",
  },
});
