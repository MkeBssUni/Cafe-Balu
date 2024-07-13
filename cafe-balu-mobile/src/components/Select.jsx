import React from "react";
import { View, StyleSheet, Text } from "react-native";
import { Picker } from "@react-native-picker/picker";

const SelectComponent = ({ label, value, setValue, list, defaultTitle }) => {
  return (
    <View>
      <Text style={styles.label}>{label}</Text>
      <View style={styles.pickerContainer}>
        <Picker
          selectedValue={value}
          style={styles.picker}
          onValueChange={(itemValue) => setValue(itemValue)}
          mode="dropdown"
          dropdownIconColor="#A6793D"
        >
        <Picker.Item label={defaultTitle} value={0} />
          {list.map((item) => (
            <Picker.Item key={item.id} value={item.id} label={item.name}/>
          ))}
        </Picker>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    margin: 20,
  },
  label: {
    color: "#8B4513",
    fontSize: 16,
    marginBottom: 10,
    fontWeight: "bold",
  },
  pickerContainer: {
    borderBottomWidth: 1,
    borderBottomColor: "#A6793D",
    borderRadius: 4,
  },
  picker: {
    height: 50,
    width: "100%",
    color: "black",
  },
});

export default SelectComponent;
