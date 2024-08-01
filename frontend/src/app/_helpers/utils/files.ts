import { HttpResponse } from "@angular/common/http";

export const downloadFile = (res: HttpResponse<any>) => {
    if (!res.body) return;
    const a = document.createElement("a");
    a.href = URL.createObjectURL(res.body);
    a.download = res.headers.get("Content-Disposition")?.split(";")[1].split("=")[1] ?? "";
    a.click();
    window.URL.revokeObjectURL(a.href);
};
