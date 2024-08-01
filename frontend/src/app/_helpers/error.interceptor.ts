import { Injectable } from "@angular/core";
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from "@angular/common/http";
import { Observable, throwError } from "rxjs";
import { catchError } from "rxjs/operators";
import { Router } from "@angular/router";

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
    constructor(private router: Router) {}

    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        return next.handle(request).pipe(
            catchError(err => {
                let status = "";
                switch (err.status) {
                    case 400:
                        status = "warn";
                        break;
                    case 401:
                        status = "warn";
                        window.alert("Unauthorized");
                        this.router.navigate(["/"]);
                        break;
                    case 403:
                        status = "error";
                        this.router.navigate(["/"]);
                        break;
                    case 404:
                        status = "error";
                        this.router.navigate(["/page-not-found"]);
                        break;
                    case 500: // Internal Server Error
                        window.alert(`Internal Server Error: ${err.error}`);
                        break;
                    //fallthrough for common error codes
                    case 501: // Not Implemented
                    case 502: // Bad Gateway
                    case 503: // Service Unavailable
                    case 504: // Gateway Timeout
                    case 505: // HTTP Version Not Supported
                    case 506: // Variant Also Negotiates (RFC 2295)
                    case 507: // Insufficient Storage (WebDAV; RFC 4918)
                    case 508: // Loop Detected (WebDAV; RFC 5842)
                    case 510: // Not Extended (RFC 2774)
                    case 511: // Network Authentication Required (RFC 6585)
                        status = "error";
                        break;
                    default: //fallthrough for error codes we let pass
                        break;
                }

                return throwError(() => new Error(err.error.error));
            })
        );
    }
}
