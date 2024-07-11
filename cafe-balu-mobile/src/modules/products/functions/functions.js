import { doGet } from "../../../config/axios";

export const getAllProducts = async () =>{
    try{
        const response = await doGet("/get_products/0")
        return response.data.products;
    }catch(error){
        console.log("response error: ", error)
        return error;
    }
}