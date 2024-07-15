import React from "react";
import Navigation from "./src/components/Navigation";
import { LogBox } from "react-native";

LogBox.ignoreAllLogs(true);
const Flex = () => {
  return (
    <Navigation />    
  );
};

export default Flex;
