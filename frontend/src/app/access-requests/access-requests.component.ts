import { Component, OnInit } from "@angular/core";
import { DefaultService, UserDataset } from "@services/api-client";

@Component({
    selector: "app-access-requests",
    templateUrl: "./access-requests.component.html",
    styleUrls: ["./access-requests.component.scss"]
})
export class AccessRequestsComponent implements OnInit {
    constructor(private service: DefaultService) {}

    userDatasets: UserDataset[] = [];

    ngOnInit(): void {
        this.reload();
    }

    reload() {
        this.service.apiGetUserDatasetsPost({ offset: 0, limit: 10 }).subscribe(res => {
            this.userDatasets = res.user_datasets;
        });
    }

    grantAccess(userDataset: UserDataset) {
        this.service
            .apiGrantAccessPost({ user_id: userDataset.user_id, dataset_id: userDataset.dataset_id })
            .subscribe(() => {
                this.reload();
            });
    }
}
