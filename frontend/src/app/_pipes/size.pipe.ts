import { Pipe, PipeTransform } from "@angular/core";
import {
    convertUnit,
    sizeToLargestPossibleBase1000Unit,
    sizeToLargestPossibleBase1024Unit,
    Unit
} from "@helpers/utils/size";

@Pipe({ name: "to_largest_base_1000_unit", standalone: true })
export class LargestBase1000UnitPipe implements PipeTransform {
    transform(size: number | null | undefined, inputUnit: Unit, separator = "."): string {
        if (size === undefined || size === null) return "";
        return sizeToLargestPossibleBase1000Unit(size, inputUnit, separator);
    }
}

@Pipe({ name: "to_largest_base_1024_unit", standalone: true })
export class LargestBase1024UnitPipe implements PipeTransform {
    transform(size: number | null | undefined, inputUnit: Unit, separator = "."): string {
        if (size === undefined || size === null) return "";
        return sizeToLargestPossibleBase1024Unit(size, inputUnit, separator);
    }
}

@Pipe({ name: "to_unit", standalone: true })
export class SizePipe implements PipeTransform {
    transform(size: number | undefined, inputUnit: Unit, outputUnit: Unit, separator = "."): string {
        if (size === undefined) return "";
        return convertUnit(size, inputUnit, outputUnit).toFixed(2).replace(".", separator);
    }
}
