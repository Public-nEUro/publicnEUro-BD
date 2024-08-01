import { Pipe, PipeTransform } from "@angular/core";

const units = ["bytes", "KB", "MB", "GB", "TB", "PB"];

@Pipe({
    name: "storage"
})
export class StoragePipe implements PipeTransform {
    transform(bytes: number): string {
        let unitIndex = 0;
        while (unitIndex + 1 < units.length && bytes > 1024) {
            bytes /= 1024;
            ++unitIndex;
        }
        return `${bytes.toFixed(2).replace(".", ",")} ${units[unitIndex]}`;
    }
}
