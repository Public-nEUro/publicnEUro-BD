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
                this.history = res.history.map(event => ({
                    timestamp: event.timestamp,
                    changedBy: event.user_id,
                    objectId: JSON.stringify(event.object_id, null, 4),
                    objectData: JSON.stringify(event.object_data, null, 4)
                }));
            });
    }
}
