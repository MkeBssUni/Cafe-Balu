import { ScrollView, StyleSheet, RefreshControl, View } from "react-native";
import React, { useEffect, useState, useCallback } from "react";
import { yearsList } from "../../../kernel/data";
import CardSale from "../../../components/CardSale";
import Select from "../../../components/Select";
import { monthsList } from "../../../kernel/data";
import { getCurrentMonth, getCurrentYear, getSalesPerDay } from "../functions/functions";
import EmptyScreen from "../../../components/EmptyScreen";
import Loading from "../../../components/Loading";

export default function AllSales() {
  const [sales, setSales] = useState([]);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedMonth, setSelectedMonth] = useState(getCurrentMonth());
  const [selectedYear, setSelectedYear] = useState(getCurrentYear());
  const [showLoading, setShowLoading] = useState(true);

  useEffect(() => {
    fetchSales();
  }, [selectedMonth, selectedYear]);

  const fetchSales = async () => {
    setShowLoading(true);
    const salesData = await getSalesPerDay(selectedMonth, selectedYear);
    setSales(salesData);
    setShowLoading(false);
  };

  const onRefresh = useCallback(() => {
    setRefreshing(true);
    fetchSales().then(() => {
      setRefreshing(false);
    });
  }, []);

  return (
    <View style={styles.container}>
        <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollViewContent}
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} colors={["#8B4513"]}/>
        }
      >
        <View style={styles.row}>
          <Select
            value={selectedMonth}
            setValue={setSelectedMonth}
            label={"Selecciona un mes"}
            list={monthsList}
            defaultTitle={"Meses"}
          />
          
          <Select
            value={selectedYear}
            setValue={setSelectedYear}
            label={"Selecciona un año"}
            list={yearsList}
            defaultTitle={"Años"}
          />
        </View>
        {showLoading ? <Loading /> : sales.length > 0 ? sales.map((sale, index) => (
          <CardSale
            key={index}
            id={sale.id}
            date={sale.createdAt}
            status={sale.status}
            total={sale.total}
            products={sale.products}
          />
        )) : <EmptyScreen title={"Sin ventas"} />}
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
  datePickerBtn: {
    backgroundColor: "#D2B48C",
    borderRadius: 10,
  },
  row: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginHorizontal: 16,
  },
  buttonContainer: {
    marginTop: 10,
    width: "40%",
    alignSelf: "center",
    marginHorizontal: 16,
  },
  imgPicker: {},
});
