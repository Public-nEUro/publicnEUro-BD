import { Pipe, PipeTransform } from "@angular/core";
import { fieldKeyOrder } from "@helpers/utils/userInfo";
import { GetUserInfoResponse } from "@services/api-client";

@Pipe({
    name: "userInfoToSortedEntries"
})
export class UserInfoToSortedEntriesPipe implements PipeTransform {
    transform<T>(userInfo: GetUserInfoResponse | Record<string, T>): { key: string; value: T }[] {
        return Object.entries(userInfo)
            .filter(([key]) => fieldKeyOrder[key] !== undefined)
            .sort((a, b) => (fieldKeyOrder[a[0]] ?? Infinity) - (fieldKeyOrder[b[0]] ?? Infinity))
            .map(([key, value]) => ({ key, value }));
    }
}
