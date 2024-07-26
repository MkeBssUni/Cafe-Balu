import axios from "axios";
import AsyncStorage from "@react-native-async-storage/async-storage";

const instance = axios.create({
    baseURL: 'https://afzd4wkj63.execute-api.us-east-2.amazonaws.com/Prod',
    timeout: 5000,
});

instance.interceptors.request.use(async (config) => {
    const token = await AsyncStorage.getItem("token");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, function (error) {
    return Promise.reject(error);
});

const handleUnauthorizedOrForbidden = () => {
    console.log("token invalido");
    AsyncStorage.removeItem("token");
};

instance.interceptors.response.use(
    response => response,
    error => {
        const { status } = error.response;
        if (status === 401 || status === 403) {
            handleUnauthorizedOrForbidden();
        }
        return Promise.reject(error);
    }
);

const doPost = async (url, data) => {
    try {
        const response = await instance.post(url, data);
        return response;
    } catch (error) {
        return error;
    }
};

const doGet = async (url) => {
    try {
        const response = await instance.get(url);
        return response;
    } catch (error) {
        return error;
    }
};

const doPut = async (url, data) => {
    try {
        const response = await instance.put(url, data);
        return response;
    } catch (error) {
        return error;
    }
};

const doPatch = async (url, data) => {
    try {
        const response = await instance.patch(url, data);
        return response;
    } catch (error) {
        return error;
    }
};

export { doPost, doGet, doPut, doPatch };
