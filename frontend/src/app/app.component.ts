import { Component } from "@angular/core";
import { UserInfo } from "@services/api-client";
import { AuthenticationService } from "@services/authentication.service";

@Component({
    selector: "app-root",
    templateUrl: "./app.component.html",
    styleUrls: ["./app.component.css"]
})
export class AppComponent {
    constructor(private authenticationService: AuthenticationService) {}

    userInfo: UserInfo | undefined = undefined;

    ngOnInit(): void {
        this.authenticationService.userInfo.subscribe(res => {
            this.userInfo = res;
        });
    }
}
