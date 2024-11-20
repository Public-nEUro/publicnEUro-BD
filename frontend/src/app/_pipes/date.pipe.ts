import { Pipe, PipeTransform } from "@angular/core";
import * as moment from "moment";

@Pipe({
    name: "date"
})
export class DatePipe implements PipeTransform {
    transform(date: Date | null | undefined): string {
        if (date === undefined || date === null) return "";
        return moment(date).format("YYYY-MM-DD");
    }
}
