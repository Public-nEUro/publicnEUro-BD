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

    users: GetUsersResponse["users"] | undefined = undefined;

    ngOnInit(): void {
        this.authenticationService.userInfo.subscribe(user => {
            if (!user) return;
            if (!user.is_admin) {
                this.router.navigate(["/"]);
                return;
            }
            this.refresh();
        });
    }

    refresh() {
        this.service.getUsersPost({}).subscribe(res => {
            console.log(res);
            this.users = res.users;
        });
    }

    approve(userId: string) {
        this.service.approveUserPost({ user_id: userId }).subscribe(() => {
            this.refresh();
        });
    }
}
