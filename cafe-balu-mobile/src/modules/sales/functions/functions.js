import { doPost } from "../../../config/axios";

export const getCurrentMonth = () => {
    const date = new Date();
    const month = date.getMonth() + 1;
    return month < 10 ? month : month;
}

export const getCurrentYear = () => {
    const date = new Date();
    return date.getFullYear();
}

const getFirstDayOfMonth = (month, year) => {
    return new Date(year, month - 1, 1);
}

const getLastDayOfMonth = (month, year) => {
    return new Date(year, month, 0);
}

const getRangeOfDates = (month, year) => {
    const firstDay = getFirstDayOfMonth(month, year);
    const lastDay = getLastDayOfMonth(month, year);

    const firstDate = `${firstDay.getFullYear()}-${firstDay.getMonth() + 1}-${firstDay.getDate()}`;
    const lastDate = `${lastDay.getFullYear()}-${lastDay.getMonth() + 1}-${lastDay.getDate()}`;

    return { firstDate, lastDate };
}


export const getSalesPerDay = async (month, year) => {
    const {firstDate, lastDate} = getRangeOfDates(month, year);

    const result = await doPost("history_per_day",{
        startDate: firstDate,
        endDate: lastDate
    });
    
    return result.data != undefined ? result.data : [];
}