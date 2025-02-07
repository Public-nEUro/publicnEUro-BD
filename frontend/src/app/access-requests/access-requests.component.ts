import { Component } from "@angular/core";
import { downloadBase64 } from "@helpers/utils/file";
import { DefaultService, UserDataset } from "@services/api-client";
import { TableLazyLoadEvent } from "primeng/table";

@Component({
    selector: "app-access-requests",
    templateUrl: "./access-requests.component.html",
    styleUrls: ["./access-requests.component.scss"]
})
export class AccessRequestsComponent {
    constructor(private service: DefaultService) {}

    userDatasets: UserDataset[] = [];
    total = 0;

    first = 0;
    rows = 10;

    loadData(offset: number, limit: number) {
        this.service.apiGetUserDatasetsPost({ offset, limit }).subscribe(res => {
            this.userDatasets = res.user_datasets;
            this.total = res.total;
        });
    }

    onLazyLoad(event: TableLazyLoadEvent) {
        this.loadData(event.first ?? 0, event.rows ?? 0);
    }

    grantAccess(userDataset: UserDataset) {
        this.service
            .apiGrantAccessPost({ user_id: userDataset.user_id, dataset_id: userDataset.dataset_id })
            .subscribe(res => {
                alert(res.status_message);
                this.loadData(this.first, this.rows);
            });
    }

    checkAccess(userDataset: UserDataset) {
        this.service
            .apiCheckAccessPost({ user_id: userDataset.user_id, dataset_id: userDataset.dataset_id })
            .subscribe(res => {
                alert(res.status_message);
                this.loadData(this.first, this.rows);
            });
    }

    deleteAccessRequest(userDataset: UserDataset) {
        if (
            !confirm(
                "You are about to delete this access request. The user will NOT be notified about this. Also, the DELPHI share will NOT be deleted by this action. After deleting this access request, the user can create a new access request if they want to."
            )
        )
            return;
        this.service
            .apiDeleteAccessRequestPost({ dataset_id: userDataset.dataset_id, user_id: userDataset.user_id })
            .subscribe(() => {
                this.loadData(this.first, this.rows);
            });
    }

    downloadSignedDua(userDataset: UserDataset) {
        if (userDataset.signed_dua_file_name === null || userDataset.signed_dua_file_data === null) return;
        downloadBase64(userDataset.signed_dua_file_data, userDataset.signed_dua_file_name);
    }
}
