import { Component, Inject, OnInit } from "@angular/core";
import { AbstractControl, UntypedFormBuilder, UntypedFormGroup, ValidationErrors, Validators } from "@angular/forms";
import { ActivatedRoute, Router } from "@angular/router";
import { fieldKeyToLabel } from "@helpers/utils/userInfo";
import { DefaultService, InstitutionWithAcceptance, RegisterRequest } from "@services/api-client";
import { RECAPTCHA_V3_SITE_KEY } from "ng-recaptcha-2";
import { map, Observable, startWith } from "rxjs";

type FieldKey = keyof RegisterRequest;

type FieldInfo = {
    type: string;
    autocomplete: string;
    validators: ((control: AbstractControl) => ValidationErrors | null)[];
    description?: string;
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
        },
        institution_name: {
            type: "autocomplete",
            autocomplete: "",
            validators: [Validators.required]
        },
        storage_protection: {
            type: "textarea",
            autocomplete: "",
            validators: [Validators.required],
            description:
                "Where will the data be stored and what security systems are in place to prevent data leaks? (e.g. on our university server which sits behind firewalls and requires user logging, on my institution desktop which requires user logging, on my laptop which has hard drive encryption and user logging)"
        },
        access_protection: {
            type: "textarea",
            autocomplete: "",
            validators: [Validators.required],
            description:
                "Only people who have signed the data user agreement related to a given dataset can use this dataset ; which measures are in place to ensure no one else will access and process data? (e.g. the data will be on my personal desktop that only I can log into, the data will be in a folder on the server with access management and only I can access)"
        }
    };

    registerForm: UntypedFormGroup;
    submitted = false;
    recaptchaSiteKey: string;
    captchaResponse: string | null = null;

    allInstitutions: InstitutionWithAcceptance[] = [];
    filteredInstitutionNames!: Observable<string[]>;
    institutionName = "";
    institution: InstitutionWithAcceptance | undefined;

    constructor(
        private router: Router,
        private route: ActivatedRoute,
        private formBuilder: UntypedFormBuilder,
        private service: DefaultService,
        @Inject(RECAPTCHA_V3_SITE_KEY) recaptchaSiteKey: string
    ) {
        this.registerForm = this.formBuilder.group(
            Object.fromEntries(Object.entries(this.field_infos).map(([key, { validators }]) => [key, ["", validators]]))
        );
        this.recaptchaSiteKey = recaptchaSiteKey;
    }

    ngOnInit() {
        this.service.apiGetInstitutionsPost({}).subscribe(res => {
            this.allInstitutions = res.institutions;
            this.filteredInstitutionNames = this.registerForm.get("institution_name")!.valueChanges.pipe(
                startWith(""),
                map((value: string) => {
                    this.institutionName = value;
                    this.institution = this.allInstitutions.find(i => i.name === value);
                    return this.allInstitutions
                        .filter(i => i.name.toLowerCase().includes(value.toLowerCase()))
                        .map(i => i.name);
                })
            );
        });
    }

    get f() {
        return this.registerForm.controls;
    }

    onCaptchaResolved(captchaResponse: string | null) {
        this.captchaResponse = captchaResponse;
    }

    onSubmit() {
        this.submitted = true;
        if (this.institutionName === "") return;
        if (this.registerForm.invalid) return;
        if (this.captchaResponse === null) return;
        const entries = Object.keys(this.field_infos).map(key => [key, this.f[key].value]);
        const registerRequestWithoutCaptcha: RegisterRequestWithoutCaptcha = Object.fromEntries(entries);
        const registerRequest: RegisterRequest = {
            ...registerRequestWithoutCaptcha,
            institution_name: this.institutionName,
            captcha_response: this.captchaResponse
        };
        this.service.apiRegisterPost(registerRequest).subscribe(() => {
            const redirect = this.route.snapshot.queryParamMap.get("redirect");
            window.location.replace(redirect ?? "/manage");
        });
    }
}
