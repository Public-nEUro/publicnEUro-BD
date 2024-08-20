import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { DefaultService } from "@services/api-client";

@Component({
    selector: "app-confirmation",
    templateUrl: "./confirmation.component.html",
    styleUrls: ["./confirmation.component.scss"]
})
export class ConfirmationComponent implements OnInit {
    response: string | undefined = undefined;

    constructor(private router: Router, private route: ActivatedRoute, private service: DefaultService) {}

    ngOnInit(): void {
        this.confirm();
    }

    getPasskey() {
        const passkey = this.route.snapshot.paramMap.get("email_confirmation_passkey");
        if (passkey === null) alert("No passkey provided");
        return passkey;
    }

    confirm() {
        const passkey = this.getPasskey();
        if (passkey === null) return;
        this.service.confirmEmailWithPasskeyPost({ passkey }).subscribe(res => {
            this.response = res.message;
            console.log(this.response);
        });
    }
}
