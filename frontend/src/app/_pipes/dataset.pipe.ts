import { Pipe, PipeTransform } from "@angular/core";
import { fieldKeyOrder } from "@helpers/utils/dataset";
import { Dataset } from "@services/api-client";

@Pipe({
    name: "datasetToSortedEntries"
})
export class DatasetToSortedEntriesPipe implements PipeTransform {
    transform<T>(dataset: Dataset | Record<string, T>): { key: string; value: T }[] {
        return Object.entries(dataset)
            .filter(([key]) => fieldKeyOrder[key] !== undefined)
            .sort((a, b) => (fieldKeyOrder[a[0]] ?? Infinity) - (fieldKeyOrder[b[0]] ?? Infinity))
            .map(([key, value]) => ({ key, value }));
    }
}
