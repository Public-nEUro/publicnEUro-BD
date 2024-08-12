import { Component, OnInit } from "@angular/core";
import { FormControl, UntypedFormBuilder, UntypedFormGroup, Validators } from "@angular/forms";
import { DefaultService, RegisterRequest } from "@services/api-client";

type FieldKey = keyof RegisterRequest;

@Component({
    selector: "app-register",
    templateUrl: "./register.component.html",
    styleUrls: ["./register.component.scss"]
})
export class RegisterComponent implements OnInit {
    field_keys: FieldKey[] = ["first_name", "last_name", "email", "address", "password"];
    field_labels: Record<FieldKey, string> = {
        first_name: "First name",
        last_name: "Last name",
        email: "Email",
        address: "Address",
        password: "Password"
    };
    field_types: Record<FieldKey, string> = {
        first_name: "text",
        last_name: "text",
        email: "text",
        address: "text",
        password: "password"
    };
    field_autocomplete: Record<FieldKey, string> = {
        first_name: "given-name",
        last_name: "family-name",
        email: "email",
        address: "address-line1",
        password: "new-password"
    };

    registerForm: UntypedFormGroup = new UntypedFormGroup(
        Object.fromEntries(this.field_keys.map(key => [key, new FormControl("")]))
    );
    submitted = false;

    constructor(private formBuilder: UntypedFormBuilder, private service: DefaultService) {}

    ngAfterViewInit(): void {}

    ngOnInit() {
        this.registerForm = this.formBuilder.group(
            Object.fromEntries(
                this.field_keys.map(key => [
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
        const entries = this.field_keys.map(key => [key, this.f[key].value]);
        this.service.registerPost(Object.fromEntries(entries)).subscribe(res => {
            console.log(res);
        });
    }
}
