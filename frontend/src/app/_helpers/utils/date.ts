import * as moment from "moment";

export const formatDate = (date: Date) => moment(date).format("YYYY-MM-DD");

export const formatQuarter = (date: Date) => {
    const q = Math.floor(date.getMonth() / 3);
    return `${date.getFullYear()} Q${q + 1}`;
};

export const quarterToStartDate = (quarter: string) => {
    const [y, m] = quarterToYearAndMonth(quarter);
    const result = new Date();
    result.setHours(0, 0, 0, 0);
    result.setDate(1);
    result.setMonth(m);
    result.setFullYear(y);
    return result;
};

export const quarterToEndDate = (quarter: string) => {
    const result = quarterToStartDate(quarter);
    result.setMonth(result.getMonth() + 3);
    result.setDate(0);
    return result;
};

export const formatInvoiceQuarter = (date: Date) => {
    if (date.getMonth() === 11 && date.getDate() > 15) return `${date.getFullYear() + 1} Q1`;
    return formatQuarter(date);
};

export const invoiceQuarterToStartDate = (quarter: string) => {
    const result = quarterToStartDate(quarter);
    if (result.getMonth() === 0) {
        result.setMonth(-1);
        result.setDate(16);
    }
    return result;
};

export const invoiceQuarterToEndDate = (quarter: string) => {
    const result = quarterToEndDate(quarter);
    if (result.getMonth() === 11) result.setDate(15);
    return result;
};

export const quarterToYearAndQ = (quarter: string) => {
    const [year, qText] = quarter.split(" ");
    return [Number(year), Number(qText[1])];
};

export const quarterToYearAndMonth = (quarter: string) => {
    const [y, q] = quarterToYearAndQ(quarter);
    return [y, (q - 1) * 3];
};

export const addQuarters = (quarter: string, count: number) => {
    const result = quarterToStartDate(quarter);
    result.setMonth(result.getMonth() + count * 3);
    return formatQuarter(result);
};
