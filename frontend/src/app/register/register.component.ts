import { Component, Inject, OnInit } from "@angular/core";
import {
    AbstractControl,
    FormControl,
    UntypedFormBuilder,
    UntypedFormGroup,
    ValidationErrors,
    Validators
} from "@angular/forms";
import { Router } from "@angular/router";
import { fieldKeyToLabel } from "@helpers/utils/userInfo";
import { DefaultService, RegisterRequest } from "@services/api-client";
import { RECAPTCHA_V3_SITE_KEY } from "ng-recaptcha-2";

type FieldKey = keyof RegisterRequest;

type FieldInfo = {
    type: string;
    autocomplete: string;
    validators: ((control: AbstractControl) => ValidationErrors | null)[];
};

type FieldInfos = Omit<Record<FieldKey, FieldInfo>, "captcha_response">;

type RegisterRequestWithoutCaptcha = Omit<RegisterRequest, "captcha_response">;

@Component({
    selector: "app-register",
    templateUrl: "./register.component.html",
    styleUrls: ["./register.component.scss"]
})
export class RegisterComponent implements OnInit {
    fieldKeyToLabel = fieldKeyToLabel;

    field_infos: FieldInfos = {
        first_name: {
            type: "text",
            autocomplete: "given-name",
            validators: [Validators.required]
        },
        last_name: {
            type: "text",
            autocomplete: "family-name",
            validators: [Validators.required]
        },
        email: {
            type: "text",
            autocomplete: "email",
            validators: [Validators.required, Validators.email]
        },
        address: {
            type: "text",
            autocomplete: "address-line1",
            validators: [Validators.required]
        },
        password: {
            type: "password",
            autocomplete: "new-password",
            validators: [Validators.required]
        }
    };

    registerForm: UntypedFormGroup = new UntypedFormGroup(
        Object.fromEntries(Object.keys(this.field_infos).map(key => [key, new FormControl("")]))
    );
    submitted = false;
    recaptchaSiteKey: string;
    captchaResponse: string | null = null;

    constructor(
        private router: Router,
        private formBuilder: UntypedFormBuilder,
        private service: DefaultService,
        @Inject(RECAPTCHA_V3_SITE_KEY) recaptchaSiteKey: string
    ) {
        this.recaptchaSiteKey = recaptchaSiteKey;
    }

    ngAfterViewInit(): void {}

    ngOnInit() {
        this.registerForm = this.formBuilder.group(
            Object.fromEntries(Object.entries(this.field_infos).map(([key, { validators }]) => [key, ["", validators]]))
        );
    }

    get f() {
        return this.registerForm.controls;
    }

    onCaptchaResolved(captchaResponse: string | null) {
        this.captchaResponse = captchaResponse;
    }

    onSubmit() {
        this.submitted = true;
        if (this.registerForm.invalid) return;
        if (this.captchaResponse === null) return;
        const entries = Object.keys(this.field_infos).map(key => [key, this.f[key].value]);
        const registerRequestWithoutCaptcha: RegisterRequestWithoutCaptcha = Object.fromEntries(entries);
        const registerRequest: RegisterRequest = {
            ...registerRequestWithoutCaptcha,
            captcha_response: this.captchaResponse
        };
        this.service.registerPost(registerRequest).subscribe(res => {
            this.router.navigate(["/"]);
        });
    }
}
