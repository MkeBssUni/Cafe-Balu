import { ScrollView, StyleSheet, Text, View } from "react-native";
import React, { useEffect, useState } from "react";
import { salesPerDay } from "../../../kernel/data";
import CardSale from "../../../components/CardSale";

export default function AllSales() {
    const [sales, setSales] = useState([]);
  useEffect(() => {
    setSales(salesPerDay);
  }, []);

  return (
    <View style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollViewContent}
        showsVerticalScrollIndicator={false}
      >
        {sales.map((sale,index)=>(
            <CardSale
              key={index}
              id={sale.id}
              date={sale.createdAt}
              status={sale.status}
              total={sale.total}
              products={sale.products}
            />
        ))}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
  },
  scrollView: {
    flex: 1,
  },
  scrollViewContent: {
    padding: 10,
  },
});
