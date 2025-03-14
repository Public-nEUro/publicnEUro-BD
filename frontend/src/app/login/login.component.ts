import { AfterViewInit, Component, ElementRef, OnInit, ViewChild } from "@angular/core";
import { UntypedFormBuilder, UntypedFormControl, UntypedFormGroup, Validators } from "@angular/forms";
import { ActivatedRoute } from "@angular/router";
import { AuthenticationService } from "@services/authentication.service";
import { InternalToastService } from "@services/internaltoast.service";

@Component({
    selector: "app-login",
    templateUrl: "./login.component.html",
    styleUrls: ["./login.component.scss"]
})
export class LoginComponent implements OnInit, AfterViewInit {
    @ViewChild("emailInput", { static: false }) emailInput!: ElementRef;
    loginForm: UntypedFormGroup = new UntypedFormGroup({
        email: new UntypedFormControl(""),
        password: new UntypedFormControl("")
    });
    submitted = false;
    error = "";

    constructor(
        private route: ActivatedRoute,
        private formBuilder: UntypedFormBuilder,
        private authenticationService: AuthenticationService,
        private ns: InternalToastService
    ) {}

    ngAfterViewInit(): void {
        this.emailInput.nativeElement.focus();
    }

    ngOnInit() {
        this.loginForm = this.formBuilder.group({
            email: ["", [Validators.required, Validators.email]],
            password: ["", [Validators.required]]
        });
    }

    get f() {
        return this.loginForm.controls;
    }

    onSubmit() {
        this.submitted = true;
        if (this.loginForm.invalid) return;
        this.authenticationService.login(
            this.f["email"].value,
            this.f["password"].value,
            this.route.snapshot.queryParamMap.get("redirect")
        );
    }

    throwError() {
        this.ns.addMessage({
            id: "errorAuth",
            icon: "fal fa-exclamation-triangle",
            summary: "Authentication error",
            detail: this.error,
            severity: "error"
        });
    }
}
