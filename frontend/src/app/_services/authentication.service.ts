import { Injectable } from "@angular/core";
import { Router } from "@angular/router";
import { BehaviorSubject, Observable } from "rxjs";
import { DefaultService, GetUserInfoResponse } from "./api-client";
import { HttpErrorResponse } from "@angular/common/http";

@Injectable({ providedIn: "root" })
export class AuthenticationService {
    private userInfoSubject: BehaviorSubject<GetUserInfoResponse | undefined> = new BehaviorSubject<
        GetUserInfoResponse | undefined
    >(undefined);
    public userInfo: Observable<GetUserInfoResponse | undefined>;

    constructor(private router: Router, private service: DefaultService) {
        this.userInfo = this.userInfoSubject.asObservable();
        this.refreshUserInfo();
    }

    getToken() {
        return localStorage.getItem("token");
    }

    setToken(token: string | null) {
        if (token === null) localStorage.removeItem("token");
        else localStorage.setItem("token", token);
    }

    refreshUserInfo() {
        if (this.getToken() === null) {
            this.userInfoSubject.next(undefined);
            return;
        }
        this.service.getUserInfoPost({}).subscribe({
            next: res => {
                this.userInfoSubject.next(res);
            },
            error: (err: HttpErrorResponse) => {
                if (err.status === 401) this.logout();
            }
        });
    }

    login(email: string, password: string) {
        this.service.loginPost({ email, password }).subscribe(res => {
            if (res.token === undefined) {
                alert(res.error_message);
                return;
            }
            this.setToken(res.token);
            this.refreshUserInfo();
            this.router.navigate(["/"]);
        });
    }

    logout() {
        this.setToken(null);
        this.refreshUserInfo();
    }
}
