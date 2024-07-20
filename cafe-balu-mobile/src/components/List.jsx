import { StyleSheet, Text, View } from 'react-native';
import React from 'react';

export default function List(props) {
  const { name, status, index } = props;
  return (
    <View style={styles.categoryContainer} key={index}>
      <Text style={styles.categoryName}>{name.length > 23 ? name.substring(0, 23) + '...' : name}</Text>
      <View style={[styles.status, status === 1 ? styles.activeStatus : styles.inactiveStatus]}>
        <Text style={styles.statusText}>{status === 1 ? 'Activa' : 'Inactiva'}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  categoryContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#fff',
    marginBottom: 16,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 2,
  },
  categoryName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#8B4513',
  },
  status: {
    paddingVertical: 4,
    paddingHorizontal: 8,
    borderRadius: 4,
  },
  activeStatus: {
    backgroundColor: '#DFF0D8',
  },
  inactiveStatus: {
    backgroundColor: '#F2DEDE',
  },
  statusText: {
    color: '#333',
  },
});
