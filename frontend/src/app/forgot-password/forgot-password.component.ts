import { AfterViewInit, Component, ElementRef, OnInit, ViewChild } from "@angular/core";
import { UntypedFormBuilder, UntypedFormControl, UntypedFormGroup, Validators } from "@angular/forms";
import { DefaultService } from "@services/api-client";

@Component({
    selector: "app-forgot-password",
    templateUrl: "./forgot-password.component.html",
    styleUrls: ["./forgot-password.component.scss"]
})
export class ForgotPasswordComponent implements OnInit, AfterViewInit {
    @ViewChild("emailInput", { static: false }) emailInput!: ElementRef;
    forgotPasswordForm: UntypedFormGroup = new UntypedFormGroup({
        email: new UntypedFormControl("")
    });
    submitted = false;
    sent = false;

    constructor(private formBuilder: UntypedFormBuilder, private service: DefaultService) {}

    ngAfterViewInit(): void {
        this.emailInput.nativeElement.focus();
    }

    ngOnInit() {
        this.forgotPasswordForm = this.formBuilder.group({
            email: ["", [Validators.required, Validators.email]]
        });
    }

    get f() {
        return this.forgotPasswordForm.controls;
    }

    onSubmit() {
        this.submitted = true;
        if (this.forgotPasswordForm.invalid) return;
        this.service.apiForgotPasswordPost({ email: this.f["email"].value }).subscribe(() => {
            this.sent = true;
        });
    }
}
