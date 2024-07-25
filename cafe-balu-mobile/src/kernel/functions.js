import AsyncStorage from "@react-native-async-storage/async-storage";

export const tokenExists = async () => {
    try {
        const token = await AsyncStorage.getItem("token");
        return token !== null;
    } catch (error) {
        return false;
    }
}
