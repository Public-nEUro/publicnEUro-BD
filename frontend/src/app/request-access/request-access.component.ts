import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { fieldKeyToLabel } from "@helpers/utils/dataset";
import { downloadBase64, toBase64 } from "@helpers/utils/file";
import { Dataset, DatasetDetails, DefaultService, UserDataset, UserInfo } from "@services/api-client";

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
    userDataset: UserDataset | null | undefined = undefined;

    acceptDua = false;

    ApprovalTypeEnum = DatasetDetails.ApprovalTypeEnum;

    signedDuaFileName: string | null = null;
    signedDuaFileData: string | null = null;

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
            next: userInfoRes => {
                this.userInfo = userInfoRes;
                const datasetId = this.getDatasetId();
                if (datasetId === null) return;
                this.service.apiGetDatasetPost({ id: datasetId }).subscribe({
                    next: datasetRes => {
                        this.dataset = datasetRes;
                        if (!this.userInfo) return;
                        this.service
                            .apiGetUserDatasetPost({ user_id: this.userInfo.id, dataset_id: datasetId })
                            .subscribe(userDataset => {
                                this.userDataset = userDataset;
                            });
                    },
                    error: err => {
                        if (err.status === 404) alert("Dataset not found");
                    }
                });
            },
            error: err => {
                if (err.status === 401) this.userInfo = null;
            }
        });
    }

    downloadDua() {
        if (this.dataset === undefined) return;
        this.service.apiGetDatasetDuaPost({ id: this.dataset?.id }).subscribe(res => {
            downloadBase64(res.file_data, res.file_name);
        });
    }

    async onSignedDuaFileSelected(event: Event) {
        const file = (event.target as HTMLInputElement).files?.[0];
        if (file === undefined) return;
        this.signedDuaFileName = file.name;
        this.signedDuaFileData = await toBase64(file);
    }

    downloadScc() {
        if (!this.dataset?.scc_id) return;
        this.service.apiGetSccPost({ id: this.dataset.scc_id }).subscribe(res => {
            downloadBase64(res.file_data, res.file_name);
        });
    }

    requestAccess() {
        this.service
            .apiRequestAccessPost({
                dataset_id: this.getDatasetId(),
                accept_dua: this.acceptDua || this.signedDuaFileName !== null,
                signed_dua_file_name: this.signedDuaFileName,
                signed_dua_file_data: this.signedDuaFileData
            })
            .subscribe(res => {
                alert(res.status_message);
            });
    }

    resendShareLink() {
        if (!this.dataset) return;
        this.service.apiResendShareLinkPost({ dataset_id: this.dataset.id }).subscribe(res => {
            alert(res.status_message);
        });
    }
}
