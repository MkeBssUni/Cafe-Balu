import { doGet, doPost } from "../../../config/axios";

export const getAllCategories = async () => {
    try {
        const response = await doGet("/get_categories/0")
        return response.data.categories;
    } catch (error) {
        console.log("error response: ", error)
        return error;
    }
}

export const newCategory = async (categoryName) => {
    try {
        const response = await doPost("/save_category",{name:categoryName});
        return response.data.message == 'CATEGORY_SAVED';
    } catch (error) {
        console.log("error response: ", error)
        return false;
    }
}