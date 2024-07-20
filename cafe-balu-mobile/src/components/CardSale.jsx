import { StyleSheet, Text, View } from "react-native";
import React from "react";
import { Card } from "@rneui/themed";
import moment from "moment";

export default function CardSale({ id, date, status, total, products }) {

    const formatedDate = moment(date).format("DD/MM/YYYY");

  return (
    <Card containerStyle={styles.card}>
      <View style={styles.rowContainer}>
        <View style={styles.dataContainer}>
          <View style={styles.row}>
            <Text style={styles.title}>Fecha venta:</Text>
            <Text style={styles.date}>{formatedDate}</Text>
          </View>
          <Card.Divider style={styles.cardDivider}/>
          <View style={styles.row}>
            <Text style={styles.total}>Total: ${total}</Text>
            <View style={[styles.status, status === 1 ? styles.completedStatus : styles.pendingStatus]}>
              <Text style={styles.statusText}>{status === 1 ? 'Completada' : 'Cancelada'}</Text>
            </View>
          </View>
          <Card.Divider style={styles.cardDivider}/>
          <View>
            <Text style={styles.subtitle}>Productos:</Text>
            {products.map((product, index) => (
              <Text key={index} style={styles.product}>{product.name} x{product.quantity} - ${product.price} c/u</Text>
            ))}
          </View>
        </View>
      </View>
    </Card>
  );
}

const styles = StyleSheet.create({
  rowContainer: {
    flex: 1,
    flexDirection: "column",
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
    justifyContent: "space-between",
    alignItems: "center",
  },
  title: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#8B4513",
  },
  date: {
    fontSize: 14,
    color: "#666",
  },
  cardDivider: {
    borderWidth: 0.5,
    marginVertical: 8,
  },
  dataContainer: {
    flex: 1,
    paddingLeft: 8,
  },
  total: {
    fontSize: 16,
    fontWeight: "bold",
    color: "#000",
  },
  status: {
    padding: 4,
    borderRadius: 4,
    height: 30,
    justifyContent: "center",
  },
  completedStatus: {
    backgroundColor: '#DFF0D8',
  },
  pendingStatus: {
    backgroundColor: '#F2DEDE',
  },
  statusText: {
    fontSize: 14,
    color: '#000',
  },
  subtitle: {
    fontSize: 16,
    fontWeight: "bold",
    color: "#8B4513",
    marginBottom: 4,
  },
  product: {
    fontSize: 14,
    color: "#666",
  },
});
