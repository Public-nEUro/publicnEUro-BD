import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { fieldKeyToLabel } from "@helpers/utils/dataset";
import { downloadBase64 } from "@helpers/utils/file";
import { Dataset, DatasetDetails, DefaultService, UserInfo } from "@services/api-client";

@Component({
    selector: "app-request-access",
    templateUrl: "./request-access.component.html",
    styleUrls: ["./request-access.component.scss"]
})
export class RequestAccessComponent implements OnInit {
    constructor(private router: Router, private route: ActivatedRoute, private service: DefaultService) {}
    AccessibilityEnum = Dataset.AccessibilityEnum;

    userInfo: UserInfo | null | undefined = undefined;

    fieldKeyToLabel = fieldKeyToLabel;

    dataset: DatasetDetails | undefined = undefined;

    acceptDua = false;

    ngOnInit(): void {
        this.refresh();
    }

    getDatasetId() {
        return this.route.snapshot.paramMap.get("dataset_id") ?? "";
    }

    gotoLogin() {
        this.router.navigate(["/login"], {
            queryParams: { redirect: window.location.pathname }
        });
    }

    gotoRegister() {
        this.router.navigate(["/register"], {
            queryParams: { redirect: window.location.pathname }
        });
    }

    refresh() {
        this.service.apiGetUserInfoPost({}).subscribe({
            next: res => {
                this.userInfo = res;
            },
            error: err => {
                if (err.status === 401) this.userInfo = null;
            }
        });
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

    requestAccess() {
        this.service
            .apiRequestAccessPost({ dataset_id: this.getDatasetId(), accept_dua: this.acceptDua })
            .subscribe(res => {
                alert(res.status_message);
            });
    }
}
