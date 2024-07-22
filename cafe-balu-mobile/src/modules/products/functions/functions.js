import { doGet, doPost } from "../../../config/axios";

export const getAllProducts = async () =>{
    try{
        const response = await doGet("/get_products/0")
        return response.data.products;
    }catch(error){
        console.log("response error: ", error)
        return error;
    }
}

export const saveProduct = async (product) =>{
    try{
        const response = await doPost("/add_product",{
            name: product.name,
            stock: product.stock,
            price: product.price,
            category_id: product.category_id,
            image: product.image
        });
        return response;
    }catch(error){
        return error;
    }
}