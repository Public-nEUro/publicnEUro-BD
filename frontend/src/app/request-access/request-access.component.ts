import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { fieldKeyToLabel } from "@helpers/utils/dataset";
import { Dataset, DefaultService, UserInfo } from "@services/api-client";

@Component({
    selector: "app-request-access",
    templateUrl: "./request-access.component.html",
    styleUrls: ["./request-access.component.scss"]
})
export class RequestAccessComponent implements OnInit {
    constructor(private router: Router, private route: ActivatedRoute, private service: DefaultService) {}

    userInfo: UserInfo | null | undefined = undefined;

    fieldKeyToLabel = fieldKeyToLabel;

    dataset: Dataset | undefined = undefined;

    ngOnInit(): void {
        this.refresh();
    }

    getDatasetId() {
        return this.route.snapshot.paramMap.get("dataset_id") ?? "";
    }

    refresh() {
        const datasetId = this.getDatasetId();
        if (datasetId === null) return;
        this.service.apiGetDatasetPost({ id: datasetId }).subscribe({
            next: res => {
                this.dataset = res;
                console.log(this.dataset);
            },
            error: err => {
                if (err.status === 404) alert("Dataset not found");
            }
        });
    }
}
