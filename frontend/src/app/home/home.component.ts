import { Component, OnInit } from "@angular/core";
import { Router } from "@angular/router";
import { fieldKeyToLabel } from "@helpers/utils/userInfo";
import { GetUserInfoResponse } from "@services/api-client";
import { AuthenticationService } from "@services/authentication.service";

@Component({
    selector: "app-home",
    templateUrl: "./home.component.html",
    styleUrls: ["./home.component.scss"]
})
export class HomeComponent implements OnInit {
    fieldKeyToLabel = fieldKeyToLabel;

    constructor(private router: Router, private authenticationService: AuthenticationService) {}

    userInfo: GetUserInfoResponse | undefined = undefined;

    ngOnInit(): void {
        this.authenticationService.userInfo.subscribe(res => {
            this.userInfo = res;
        });
    }

    register() {
        this.router.navigate(["/register"]);
    }

    login() {
        this.router.navigate(["/login"]);
    }

    logout() {
        this.authenticationService.logout();
    }
}
