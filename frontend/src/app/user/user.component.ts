import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { fieldKeyToLabel } from "@helpers/utils/userInfo";
import { DefaultService, UserInfo } from "@services/api-client";

@Component({
    selector: "app-user",
    templateUrl: "./user.component.html",
    styleUrls: ["./user.component.scss"]
})
export class UserComponent implements OnInit {
    fieldKeyToLabel = fieldKeyToLabel;

    constructor(private router: Router, private route: ActivatedRoute, private service: DefaultService) {}

    userInfo: UserInfo | null | undefined = undefined;

    ngOnInit(): void {
        this.refresh();
    }

    getUserId() {
        const userId = this.route.snapshot.paramMap.get("user_id");
        if (userId === null) alert("No user ID provided");
        return userId;
    }

    refresh() {
        const userId = this.getUserId();
        if (userId === null) return;
        this.service.apiGetUserInfoByIdPost({ user_id: userId }).subscribe({
            next: res => {
                this.userInfo = res;
            },
            error: err => {
                if (err.status === 404) this.userInfo = null;
                if (err.status === 401)
                    this.router.navigate(["/login"], {
                        queryParams: { redirect: window.location.pathname }
                    });
            }
        });
    }

    approve() {
        if (!this.userInfo) return;
        const userId = this.getUserId();
        if (userId === null) return;
        this.service.apiApproveUserPost({ user_id: this.userInfo.id }).subscribe(() => {
            this.refresh();
        });
    }

    reject() {
        if (!this.userInfo) return;
        const userId = this.getUserId();
        if (userId === null) return;
        this.service.apiRejectUserPost({ user_id: this.userInfo.id }).subscribe(() => {
            this.refresh();
        });
    }
}
