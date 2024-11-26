import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { fieldKeyToLabel } from "@helpers/utils/dataset";
import { Dataset, DefaultService } from "@services/api-client";

@Component({
    selector: "app-dataset",
    templateUrl: "./dataset.component.html",
    styleUrls: ["./dataset.component.scss"]
})
export class DatasetComponent implements OnInit {
    fieldKeyToLabel = fieldKeyToLabel;

    constructor(private router: Router, private route: ActivatedRoute, private service: DefaultService) {}

    dataset: Dataset | null | undefined = undefined;

    ngOnInit(): void {
        this.refresh();
    }

    getDatasetId() {
        const datasetId = this.route.snapshot.paramMap.get("dataset_id");
        if (datasetId === null) alert("No dataset ID provided");
        return datasetId;
    }

    refresh() {
        const datasetId = this.getDatasetId();
        if (datasetId === null) return;
        this.service.apiGetDatasetPost({ id: datasetId }).subscribe({
            next: res => {
                this.dataset = res;
            },
            error: err => {
                if (err.status === 404) this.dataset = null;
                if (err.status === 401)
                    this.router.navigate(["/login"], {
                        queryParams: { redirect: window.location.pathname }
                    });
            }
        });
    }
}
