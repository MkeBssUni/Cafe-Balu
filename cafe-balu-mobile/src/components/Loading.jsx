import { StyleSheet, Text, View, ActivityIndicator } from 'react-native'
import React from 'react'

export default function Loading() {
  return (
    <View style={styles.container}>
    <ActivityIndicator
        size="large"
        color="#8B4513"
    />
    </View>
  )
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
    }
})