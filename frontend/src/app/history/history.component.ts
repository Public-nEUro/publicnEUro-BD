import { Component } from "@angular/core";
import { DefaultService } from "@services/api-client";
import { TableLazyLoadEvent } from "primeng/table";

type HistoryEvent = {
    timestamp: string;
    changedBy: string;
    objectId: string;
    objectData: string;
};

@Component({
    selector: "app-history",
    templateUrl: "./history.component.html",
    styleUrls: ["./history.component.scss"]
})
export class HistoryComponent {
    constructor(private service: DefaultService) {}

    history: HistoryEvent[] = [];
    total = 0;

    first = 0;
    rows = 10;

    loadData(offset: number, limit: number) {
        this.service
            .apiGetHistoryPost({
                offset,
                limit
            })
            .subscribe(res => {
                this.history = res.history.map(event => {
                    const changedBy = event.user_info
                        ? event.user_info.first_name + " " + event.user_info.last_name
                        : "";
                    return {
                        timestamp: event.timestamp,
                        changedBy,
                        objectId: JSON.stringify(event.object_id, null, 4),
                        objectData: JSON.stringify(event.object_data, null, 4)
                    };
                });
                this.total = res.total;
            });
    }

    onLazyLoad(event: TableLazyLoadEvent) {
        this.loadData(event.first ?? 0, event.rows ?? 0);
    }
}
