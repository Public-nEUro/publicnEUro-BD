import { Component, OnInit } from "@angular/core";
import { MatAutocompleteSelectedEvent } from "@angular/material/autocomplete";
import { ActivatedRoute } from "@angular/router";
import { DefaultService, UserDataset, UserInfo } from "@services/api-client";

@Component({
    selector: "app-dataset-users",
    templateUrl: "./dataset-users.component.html",
    styleUrls: ["./dataset-users.component.scss"]
})
export class DatasetUsersComponent implements OnInit {
    constructor(private route: ActivatedRoute, private service: DefaultService) {}

    userDatasets: UserDataset[] = [];

    users: UserInfo[] = [];
    filteredUsers: UserInfo[] = [];
    selectedUser: UserInfo | null = null;
    userSearchText = "";

    ngOnInit(): void {
        this.reload();
    }

    getDatasetId() {
        const datasetId = this.route.snapshot.paramMap.get("dataset_id");
        if (datasetId === null) alert("No dataset ID provided");
        return datasetId;
    }

    reload() {
        this.userSearchText = "";
        const datasetId = this.getDatasetId();
        if (datasetId === null) return;
        this.service.apiGetUserDatasetsForDatasetPost({ dataset_id: datasetId }).subscribe(res => {
            this.userDatasets = res.user_datasets;
        });
        this.service.apiGetApprovedUsersPost({}).subscribe(res => {
            this.users = res.users;
            this.filteredUsers = this.users;
        });
    }

    onUserSearchChange(text: string) {
        this.filteredUsers = this.users.filter(u =>
            [u.email, u.first_name, u.last_name].some(t => t.toLowerCase().includes(text.toLowerCase()))
        );
    }

    addUser() {
        this.reload();
    }

    selectUser(event: MatAutocompleteSelectedEvent) {
        const datasetId = this.getDatasetId();
        if (datasetId === null) return;
        if (
            !window.confirm(
                `Are you sure that you want to give this user access to the dataset: ${event.option.value}?`
            )
        )
            return;
        this.service.apiGrantAccessPost({ dataset_id: datasetId, user_id: event.option.id }).subscribe(() => {
            this.reload();
        });
    }
}
