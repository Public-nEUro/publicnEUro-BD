import { Pipe, PipeTransform } from "@angular/core";
import * as moment from "moment";

@Pipe({
    name: "datetime"
})
export class DatetimePipe implements PipeTransform {
    transform(date: Date | undefined): string {
        console.log(date);
        if (date === undefined) return "";
        return moment(date).format("YYYY-MM-DD HH:mm:ss");
    }
}
