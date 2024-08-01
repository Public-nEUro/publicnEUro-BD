import { LazyLoadEvent } from "primeng/api";

export type TableData<T> = {
    count: number;
    entries: T[];
    offset: number;
    pageSize: number;
    sortField: string;
    sortOrder: number;
};

export const emptyTableData = () => ({
    count: 0,
    entries: [],
    offset: 0,
    pageSize: 1000,
    sortField: "",
    sortOrder: 0
});

export const updateTableData = <T>(tableData: TableData<T>, event: LazyLoadEvent) => {
    tableData.offset = event.first ?? tableData.offset;
    tableData.sortField = event.sortField ?? tableData.sortField;
    tableData.sortOrder = event.sortOrder ?? tableData.sortOrder;
};
