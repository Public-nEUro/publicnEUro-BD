import { Component, OnInit } from "@angular/core";
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

type FieldKey = keyof RegisterRequest;

type FieldInfo = {
    type: string;
    autocomplete: string;
    validators: ((control: AbstractControl) => ValidationErrors | null)[];
};

@Component({
    selector: "app-register",
    templateUrl: "./register.component.html",
    styleUrls: ["./register.component.scss"]
})
export class RegisterComponent implements OnInit {
    fieldKeyToLabel = fieldKeyToLabel;

    field_infos: Record<FieldKey, FieldInfo> = {
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

    constructor(private router: Router, private formBuilder: UntypedFormBuilder, private service: DefaultService) {}

    ngAfterViewInit(): void {}

    ngOnInit() {
        this.registerForm = this.formBuilder.group(
            Object.fromEntries(Object.entries(this.field_infos).map(([key, { validators }]) => [key, ["", validators]]))
        );
    }

    get f() {
        return this.registerForm.controls;
    }

    onSubmit() {
        this.submitted = true;
        if (this.registerForm.invalid) return;
        const entries = Object.keys(this.field_infos).map(key => [key, this.f[key].value]);
        this.service.registerPost(Object.fromEntries(entries)).subscribe(res => {
            this.router.navigate(["/"]);
        });
    }
}
