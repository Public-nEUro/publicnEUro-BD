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

type Tooltip = {
    bold: string;
    italic: string;
    normal: string;
};

type FieldInfo = {
    type: string;
    autocomplete: string;
    validators: ((control: AbstractControl) => ValidationErrors | null)[];
    tooltip?: Tooltip;
};

type FieldInfos = Omit<Record<FieldKey, FieldInfo>, "captcha_response">;

type RegisterRequestWithoutCaptcha = Omit<RegisterRequest, "captcha_response">;

const boldProtectionText = "Data Protection Impact Assessment";
const italicProtectionText =
    "As personal data are being transfered, some authors need to assess what impact this can have.";

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
        },
        storage_protection: {
            type: "textarea",
            autocomplete: "",
            validators: [Validators.required],
            tooltip: {
                bold: boldProtectionText,
                italic: italicProtectionText,
                normal: "Where will the data be stored and what security systems are in place to prevent data leaks? (e.g. on our university server which sits behind firewalls and requires user logging, on my institution desktop which requires user logging, on my laptop which has hard drive encryption and user logging)"
            }
        },
        access_protection: {
            type: "textarea",
            autocomplete: "",
            validators: [Validators.required],
            tooltip: {
                bold: boldProtectionText,
                italic: italicProtectionText,
                normal: "Only people who have signed the data user agreement related to a given dataset can use this dataset ; which measures are in place to ensure no one else will access and process data? (e.g. the data will be on my personal desktop that only I can log into, the data will be in a folder on the server with access management and only I can access)"
            }
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
        this.service.apiRegisterPost(registerRequest).subscribe(res => {
            this.router.navigate(["/"]);
        });
    }
}
