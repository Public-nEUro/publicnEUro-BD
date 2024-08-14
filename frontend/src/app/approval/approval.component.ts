import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { fieldKeyToLabel } from "@helpers/utils/userInfo";
import { DefaultService, GetUserInfoResponse } from "@services/api-client";

@Component({
    selector: "app-approval",
    templateUrl: "./approval.component.html",
    styleUrls: ["./approval.component.scss"]
})
export class ApprovalComponent implements OnInit {
    fieldKeyToLabel = fieldKeyToLabel;

    constructor(private router: Router, private route: ActivatedRoute, private service: DefaultService) {}

    userInfo: GetUserInfoResponse | null | undefined = undefined;

    ngOnInit(): void {
        this.refresh();
    }

    getPasskey() {
        const passkey = this.route.snapshot.paramMap.get("approver_passkey");
        if (passkey === null) alert("No passkey provided");
        return passkey;
    }

    refresh() {
        const passkey = this.getPasskey();
        if (passkey === null) return;
        this.service.getUserInfoFromPasskeyPost({ passkey }).subscribe({
            next: res => {
                this.userInfo = res;
            },
            error: err => {
                if (err.status === 404) this.userInfo = null;
            }
        });
    }

    approve() {
        if (!this.userInfo) return;
        const passkey = this.getPasskey();
        if (passkey === null) return;
        this.service.approveUserWithPasskeyPost({ user_id: this.userInfo.id, passkey }).subscribe(() => {
            this.refresh();
        });
    }

    reject() {
        if (!this.userInfo) return;
        const passkey = this.getPasskey();
        if (passkey === null) return;
        this.service.rejectUserWithPasskeyPost({ user_id: this.userInfo.id, passkey }).subscribe(() => {
            this.refresh();
        });
    }
}
