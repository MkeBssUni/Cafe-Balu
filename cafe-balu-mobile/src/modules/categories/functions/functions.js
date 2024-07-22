import { doGet, doPost } from "../../../config/axios";

export const getAllCategories = async (status) => {
    try {
        if (status == undefined) status = 0;
        const response = await doGet(`/get_categories/${status}`);
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