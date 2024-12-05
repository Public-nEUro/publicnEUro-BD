import { Component } from "@angular/core";
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
}
