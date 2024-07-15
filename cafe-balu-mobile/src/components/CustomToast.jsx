import React, { useState, useEffect } from "react";
import { View, Text, Animated, StyleSheet, Dimensions } from "react-native";
import { Icon } from '@rneui/base';

const CustomToast = ({ message, iconName, iconColor, toastColor, onHide, visible, }) => {
  const [fadeAnim] = useState(new Animated.Value(0));

  useEffect(() => {
    if (visible) {
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 500,
        useNativeDriver: true,
      }).start(() => {
        setTimeout(() => {
          hideToast();
        }, 2000);
      });
    }
  }, [visible]);

  const hideToast = () => {
    Animated.timing(fadeAnim, {
      toValue: 0,
      duration: 500,
      useNativeDriver: true,
    }).start(() => {
      onHide();
    });
  };

  return (
    visible && (
      <Animated.View style={[styles.toast, { opacity: fadeAnim, backgroundColor: toastColor }]}>
        <View style={{ flexDirection: 'row', alignItems: 'center' }}>
          <Icon
            name={iconName}
            type="material-community"
            size={20}
            color={iconColor}
          />
          <Text style={[styles.toastText, { color: iconColor, marginLeft: 10 }]}>{message}</Text>
        </View>
      </Animated.View>
    )
  );
};

const styles = StyleSheet.create({
  toast: {
    position: "absolute",
    bottom: 10,
    left: Dimensions.get("window").width * 0.20,
    width: Dimensions.get("window").width * 0.6,
    padding: 8,
    borderRadius: 8,
    alignItems: "center",
  },
  toastText: {
    fontSize: 14,
  },
});

export default CustomToast;
