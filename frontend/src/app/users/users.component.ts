import { Component, OnInit } from "@angular/core";
import { DefaultService, GetUsersResponse } from "@services/api-client";

@Component({
    selector: "app-users",
    templateUrl: "./users.component.html",
    styleUrls: ["./users.component.scss"]
})
export class UsersComponent implements OnInit {
    constructor(private service: DefaultService) {}

    approvedUsers: GetUsersResponse["users"] | undefined = undefined;
    nonApprovedUsers: GetUsersResponse["users"] | undefined = undefined;

    ngOnInit() {
        this.service.apiGetApprovedUsersPost({}).subscribe(res => {
            this.approvedUsers = res.users;
            this.service.apiGetNonApprovedUsersPost({}).subscribe(res => {
                this.nonApprovedUsers = res.users;
            });
        });
    }
}
