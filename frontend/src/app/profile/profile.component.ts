import { Component, OnInit } from "@angular/core";
import { Router } from "@angular/router";
import { fieldKeyToLabel } from "@helpers/utils/userInfo";
import { UserInfo } from "@services/api-client";
import { AuthenticationService } from "@services/authentication.service";

@Component({
    selector: "app-profile",
    templateUrl: "./profile.component.html",
    styleUrls: ["./profile.component.scss"]
})
export class ProfileComponent implements OnInit {
    fieldKeyToLabel = fieldKeyToLabel;

    constructor(private router: Router, private authenticationService: AuthenticationService) {}

    userInfo: UserInfo | undefined = undefined;

    ngOnInit(): void {
        this.authenticationService.userInfo.subscribe(res => {
            this.userInfo = res;
        });
    }

    logout() {
        this.authenticationService.logout();
    }
}
