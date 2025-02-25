import { AfterViewInit, Component, ElementRef, ViewChild } from "@angular/core";
import { UntypedFormBuilder, UntypedFormControl, UntypedFormGroup, Validators } from "@angular/forms";
import { ActivatedRoute } from "@angular/router";
import { matchFields, passwordStrengthValidator } from "@helpers/utils/form";
import { DefaultService } from "@services/api-client";

@Component({
    selector: "app-reset-password",
    templateUrl: "./reset-password.component.html",
    styleUrls: ["./reset-password.component.scss"]
})
export class ResetPasswordComponent implements AfterViewInit {
    @ViewChild("passwordInput", { static: false }) passwordInput!: ElementRef;
    resetPasswordForm: UntypedFormGroup = new UntypedFormGroup({
        password: new UntypedFormControl(""),
        repeatPassword: new UntypedFormControl("")
    });
    passwordStrength = "";
    submitted = false;
    hasBeenReset = false;

    constructor(
        private route: ActivatedRoute,
        private formBuilder: UntypedFormBuilder,
        private service: DefaultService
    ) {
        this.resetPasswordForm = this.formBuilder.group(
            {
                password: ["", [Validators.required, passwordStrengthValidator(this)]],
                repeatPassword: ["", Validators.required]
            },
            { validators: [matchFields("password", "repeatPassword")] }
        );
    }

    ngAfterViewInit(): void {
        this.passwordInput.nativeElement.focus();
    }

    getPasskey() {
        const passkey = this.route.snapshot.paramMap.get("email_confirmation_passkey");
        if (passkey === null) alert("No passkey provided");
        return passkey;
    }

    get f() {
        return this.resetPasswordForm.controls;
    }

    onSubmit() {
        this.submitted = true;
        if (this.resetPasswordForm.invalid) return;

        const passkey = this.getPasskey();
        if (passkey === null) return;

        this.service
            .apiResetPasswordWithPasskeyPost({ passkey, new_password: this.f["password"].value })
            .subscribe(() => {
                this.hasBeenReset = true;
            });
    }
}
