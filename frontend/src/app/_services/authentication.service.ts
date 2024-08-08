import { Injectable } from "@angular/core";
import { Router } from "@angular/router";
import { BehaviorSubject, map, Observable } from "rxjs";
import { DefaultService } from "./api-client";

@Injectable({ providedIn: "root" })
export class AuthenticationService {
    private tokenSubject: BehaviorSubject<string> = new BehaviorSubject<string>("");
    public tokenResponse: Observable<string>;

    constructor(private router: Router, private service: DefaultService) {
        this.tokenResponse = this.tokenSubject.asObservable();
        const token = localStorage.getItem("token") ?? "";
        this.tokenSubject.next(token);
        this.checkExpired(token);
    }

    checkExpired(token: string) {
        if (token === "qwe") this.logout();
    }

    login(email: string, password: string) {
        this.logout();
        this.service.loginPost({ email, password }).subscribe(res => {
            localStorage.setItem("token", res.token);
        });
    }

    logout() {
        localStorage.removeItem("token");
        this.tokenSubject.next("");
        this.router.navigate(["/"]);
    }
}
