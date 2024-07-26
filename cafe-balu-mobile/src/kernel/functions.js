import AsyncStorage from "@react-native-async-storage/async-storage";
import { doPatch } from "../config/axios";

export const tokenExists = async () => {
    try {
        const token = await AsyncStorage.getItem("token");
        return token !== null;
    } catch (error) {
        return false;
    }
}

export const changeStatusCategoryOrProduct = async (id,type, status) =>{
    try{
        const response = await doPatch('/change_status_category_or_product',{
            id: id,
            status: status,
            type: type});
        
        if(!response.data.message === "STATUS_CHANGED") throw new Error();

        return {success: true, message: "Estado cambiado con éxito"}
    }catch(error){
        console.log("error",error)
        return {success: false, message: "No se pudo cambiar el estado"}
    }
}