import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";

import { AppRoutingModule } from "./app-routing.module";
import { AppComponent } from "./app.component";

import { HttpClientModule, HTTP_INTERCEPTORS } from "@angular/common/http";

import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { InputTextModule } from "primeng/inputtext";
import { AutoCompleteModule } from "primeng/autocomplete";
import { DropdownModule } from "primeng/dropdown";
import { TableModule } from "primeng/table";
import { CheckboxModule } from "primeng/checkbox";
import { AccordionModule } from "primeng/accordion";
import { ToolbarModule } from "primeng/toolbar";
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { ButtonModule } from "primeng/button";
import { MenuModule } from "primeng/menu";
import { CalendarModule } from "primeng/calendar";
import { ChartModule } from "primeng/chart";
import { FileUploadModule } from "primeng/fileupload";
import { StoragePipe } from "./_pipes/storage.pipe";
import { DatePipe } from "./_pipes/date.pipe";
import { DatetimePipe } from "./_pipes/datetime.pipe";
import { UserInfoToSortedEntriesPipe } from "./_pipes/userInfo.pipe";
import { ErrorInterceptor, JwtInterceptor } from "./_helpers";
import { CommonModule } from "@angular/common";
import { HomeComponent } from "./home/home.component";
import { RegisterComponent } from "./register/register.component";
import { LoginComponent } from "./login/login.component";
import { ProfileComponent } from "./profile/profile.component";
import { UsersComponent } from "./users/users.component";
import { ConfirmationComponent } from "./confirmation/confirmation.component";
import { ApprovalComponent } from "./approval/approval.component";
import { BASE_PATH } from "@services/api-client";
import { environment } from "@environments/environment";
import { MatSidenavModule } from "@angular/material/sidenav";
import { MatToolbarModule } from "@angular/material/toolbar";
import { MatIconModule } from "@angular/material/icon";
import { MatListModule } from "@angular/material/list";
import { MatFormFieldModule } from "@angular/material/form-field";
import { MatInputModule } from "@angular/material/input";
import { MatGridListModule } from "@angular/material/grid-list";
import { MatCardModule } from "@angular/material/card";
import { RECAPTCHA_V3_SITE_KEY, RecaptchaModule } from "ng-recaptcha-2";

@NgModule({
    declarations: [
        AppComponent,
        HomeComponent,
        RegisterComponent,
        LoginComponent,
        ProfileComponent,
        UsersComponent,
        ConfirmationComponent,
        ApprovalComponent,
        StoragePipe,
        DatePipe,
        DatetimePipe,
        UserInfoToSortedEntriesPipe
    ],
    imports: [
        CommonModule,
        BrowserModule,
        AppRoutingModule,
        HttpClientModule,
        FormsModule,
        ReactiveFormsModule,
        InputTextModule,
        AutoCompleteModule,
        DropdownModule,
        TableModule,
        CheckboxModule,
        AccordionModule,
        ToolbarModule,
        BrowserAnimationsModule,
        ButtonModule,
        MenuModule,
        CalendarModule,
        ChartModule,
        FileUploadModule,
        MatSidenavModule,
        MatToolbarModule,
        MatIconModule,
        MatListModule,
        RecaptchaModule,
        MatFormFieldModule,
        MatInputModule,
        MatGridListModule,
        MatCardModule,
        BrowserAnimationsModule
    ],
    providers: [
        { provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true },
        { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },
        { provide: BASE_PATH, useValue: environment.API_BASE_URL },
        { provide: RECAPTCHA_V3_SITE_KEY, useValue: environment.RECAPTCHA_V3_SITE_KEY }
    ],
    bootstrap: [AppComponent]
})
export class AppModule {}
