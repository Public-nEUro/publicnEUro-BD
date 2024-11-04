import { Pipe, PipeTransform } from "@angular/core";

@Pipe({
    name: "boolToCheckmark"
})
export class BoolToCheckmarkPipe implements PipeTransform {
    transform(value: boolean | null | undefined): string {
        if (value === true) return "✓";
        if (value === false) return "✘";
        return "?";
    }
}
