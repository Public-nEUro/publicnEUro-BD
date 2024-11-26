import { Component, OnInit } from "@angular/core";
import { Router } from "@angular/router";
import { DefaultService, GetUsersResponse } from "@services/api-client";
import { AuthenticationService } from "@services/authentication.service";

@Component({
    selector: "app-users",
    templateUrl: "./users.component.html",
    styleUrls: ["./users.component.scss"]
})
export class UsersComponent implements OnInit {
    constructor(
        private router: Router,
        private authenticationService: AuthenticationService,
        private service: DefaultService
    ) {}

    approvedUsers: GetUsersResponse["users"] | undefined = undefined;
    nonApprovedUsers: GetUsersResponse["users"] | undefined = undefined;

    ngOnInit(): void {
        this.refresh();
    }

    refresh() {
        this.service.apiGetApprovedUsersPost({}).subscribe(res => {
            this.approvedUsers = res.users;
            this.service.apiGetNonApprovedUsersPost({}).subscribe(res => {
                this.nonApprovedUsers = res.users;
            });
        });
    }
}
