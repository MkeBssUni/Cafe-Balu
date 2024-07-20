import { StyleSheet, Text, View } from 'react-native';
import React from 'react';
import { emptyImg } from '../../assets/imgs';
import { Image } from '@rneui/base';

export default function EmptyScreen({ title }) {
  return (
    <View style={styles.centerNull}>
      <Text style={styles.null}>{title}</Text>
      <Image
        source={{ uri: emptyImg }}
        style={styles.notFound}
        containerStyle={styles.containerNotFound}
        resizeMode="contain"
      />
    </View>
  );
}

const styles = StyleSheet.create({
  centerNull: {
    justifyContent: 'center',
    alignItems: 'center',
    flex: 1,
  },
  notFound: {
    width: 400,
    height: 400,
  },
  containerNotFound: {
    
  },
  null: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    color: '#8C8B8A',
    marginTop: 125,
  },
});
