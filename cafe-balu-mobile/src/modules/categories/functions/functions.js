import { doGet } from "../../../config/axios";

export const getAllCategories = async () => {
    try {
        const response = await doGet("/get_categories/0")
        return response.data.categories;
    } catch (error) {
        console.log("error response: ", error)
        return error;
    }
}