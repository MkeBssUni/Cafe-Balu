import { ScrollView, StyleSheet, Text, View } from "react-native";
import React, { useEffect, useState } from "react";
import { salesPerDay } from "../../../kernel/data";
import CardSale from "../../../components/CardSale";
import DateTimePicker from "@react-native-community/datetimepicker";
import { Button } from "@rneui/base";

export default function AllSales() {
  const [sales, setSales] = useState([]);

  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  const [mode, setMode] = useState("date");
  const [showStartDate, setShowStartDate] = useState(false);
  const [showEndDate, setShowEndDate] = useState(false);

  const onChangeStartDate = (event, selectedDate) => {
    setShowStartDate(false);
    setStartDate(selectedDate);
  };

  const onChangeEndDate = (event, selectedDate) => {
    setShowEndDate(false);
    setEndDate(selectedDate);
  };

  const showModeStart = (currentMode) => {
    setShowStartDate(true);
    setMode(currentMode);
  };

  const showModeEnd = (currentMode) => {
    setShowEndDate(true);
    setMode(currentMode);
  };

  const showDatepickerStart = () => {
    showModeStart("date");
  };

  const showDatepickerEnd = () => {
    showModeEnd("date");
  }

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
        <View style={styles.row}>
          <Button
            onPress={showDatepickerStart}
            title="Fecha inicio"
            buttonStyle={styles.datePickerBtn}
            containerStyle={styles.buttonContainer}
            iconRight={true}
            icon={{
              name: 'calendar-start',
              type: 'material-community',
              size: 22,
              color: 'white',
            }}
          />
          <Button
            onPress={showDatepickerEnd}
            title="Fecha fin"
            buttonStyle={styles.datePickerBtn}
            containerStyle={styles.buttonContainer}
            iconRight={true}
            icon={{
              name: 'calendar-end',
              type: 'material-community',
              size: 22,
              color: 'white',
            }}
          />
        </View>
        {showStartDate && (
          <DateTimePicker
            testID="dateTimePickerStart"
            value={startDate}
            mode={mode}
            is24Hour={true}
            style={styles.imgPicker}
            onChange={onChangeStartDate}
          />
        )}
        
        {showEndDate && (
          <DateTimePicker
            testID="dateTimePickerEnd"
            value={endDate}
            mode={mode}
            is24Hour={true}
            style={styles.imgPicker}
            onChange={onChangeEndDate}
            maximumDate={new Date()}
            minimumDate={startDate}
          />
        )}


        {sales.map((sale, index) => (
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
  datePickerBtn: {
    backgroundColor: "#D2B48C",
    borderRadius: 10,
  },
  row: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  buttonContainer: {
    marginTop: 10,
    width: "40%",
    alignSelf: "center",
    marginHorizontal: 16
  },
  imgPicker:{
  }
});