import { Component, OnInit } from "@angular/core";
import { FormControl, UntypedFormBuilder, UntypedFormGroup, Validators } from "@angular/forms";
import { DefaultService, RegisterRequest } from "@services/api-client";

type FieldKey = keyof RegisterRequest;

type FieldInfo = {
    label: string;
    type: string;
    autocomplete: string;
};

@Component({
    selector: "app-register",
    templateUrl: "./register.component.html",
    styleUrls: ["./register.component.scss"]
})
export class RegisterComponent implements OnInit {
    field_infos: Record<FieldKey, FieldInfo> = {
        first_name: { label: "First name", type: "text", autocomplete: "given-name" },
        last_name: { label: "Last name", type: "text", autocomplete: "family-name" },
        email: { label: "Email", type: "text", autocomplete: "email" },
        address: { label: "Address", type: "text", autocomplete: "address-line1" },
        password: { label: "Password", type: "password", autocomplete: "new-password" }
    };

    registerForm: UntypedFormGroup = new UntypedFormGroup(
        Object.fromEntries(Object.keys(this.field_infos).map(key => [key, new FormControl("")]))
    );
    submitted = false;

    constructor(private formBuilder: UntypedFormBuilder, private service: DefaultService) {}

    ngAfterViewInit(): void {}

    ngOnInit() {
        this.registerForm = this.formBuilder.group(
            Object.fromEntries(
                Object.keys(this.field_infos).map(key => [
                    key,
                    ["", key === "email" ? [Validators.required, Validators.email] : [Validators.required]]
                ])
            )
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
            console.log(res);
        });
    }
}
