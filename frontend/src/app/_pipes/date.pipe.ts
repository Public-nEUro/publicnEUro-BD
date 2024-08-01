import { Pipe, PipeTransform } from "@angular/core";
import * as moment from "moment";

@Pipe({
    name: "date"
})
export class DatePipe implements PipeTransform {
    transform(date: Date | undefined): string {
        if (date === undefined) return "";
        return moment(date).format("YYYY-MM-DD");
    }
}
