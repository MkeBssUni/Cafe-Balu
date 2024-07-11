import { ScrollView, StyleSheet, View, RefreshControl } from 'react-native'
import React, {useState, useEffect, useCallback} from 'react'
import { categoriesList } from '../../../kernel/data';
import List from '../../../components/List';
import { getAllCategories } from '../functions/functions';

export default function AllCategories() {
  const [categories, setCategories] = useState(categoriesList);
  const [refreshing, setRefreshing] = useState(false)

  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () =>{
    try {
      const categoriesList = await getAllCategories();
      setCategories(categoriesList);
    } catch (error) {
      console.log("error categories: ", error)
    }
  }

  const onRefresh = useCallback(() => {
    setRefreshing(true);
    loadCategories().then(() => {
      setRefreshing(false);
    });
  }, []);

  return (
    <View style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scrollViewContent}
        refreshControl={
          <RefreshControl refreshing = {refreshing}  onRefresh={onRefresh} />
        }
      >{
        categories.map((category, index) => (
          <List
            name = {category.name}
            status = {category.status}
          />
        ))
      }
      </ScrollView>
    </View>
  )
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