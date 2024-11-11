import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { fieldKeyToLabel } from "@helpers/utils/dataset";
import { downloadBase64 } from "@helpers/utils/file";
import { DatasetDetails, DefaultService, UserInfo } from "@services/api-client";

@Component({
    selector: "app-request-access",
    templateUrl: "./request-access.component.html",
    styleUrls: ["./request-access.component.scss"]
})
export class RequestAccessComponent implements OnInit {
    constructor(private router: Router, private route: ActivatedRoute, private service: DefaultService) {}

    userInfo: UserInfo | null | undefined = undefined;

    fieldKeyToLabel = fieldKeyToLabel;

    dataset: DatasetDetails | undefined = undefined;

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

    downloadDua() {
        if (this.dataset === undefined) return;
        this.service.apiGetDatasetDuaPost({ id: this.dataset?.id }).subscribe(res => {
            downloadBase64(res.file_data, res.file_name);
        });
    }

    downloadScc() {
        if (!this.dataset?.scc_id) return;
        this.service.apiGetSccPost({ id: this.dataset.scc_id }).subscribe(res => {
            downloadBase64(res.file_data, res.file_name);
        });
    }
}
