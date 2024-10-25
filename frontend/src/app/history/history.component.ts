import { Component, OnInit } from "@angular/core";
import { DefaultService } from "@services/api-client";
import * as moment from "moment";

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
export class HistoryComponent implements OnInit {
    constructor(private service: DefaultService) {}

    history: HistoryEvent[] = [];

    ngOnInit(): void {
        this.reload();
    }

    reload() {
        this.service
            .apiGetHistoryPost({
                start_date: moment().subtract(7, "day").toISOString(),
                end_date: moment().toISOString()
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
            });
    }
}
