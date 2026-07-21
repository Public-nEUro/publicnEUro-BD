import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";

import { AppRoutingModule } from "./app-routing.module";
import { AppComponent } from "./app.component";

import { HTTP_INTERCEPTORS, HttpClientModule } from "@angular/common/http";

import { CommonModule } from "@angular/common";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { MatAutocompleteModule } from "@angular/material/autocomplete";
import { MatCardModule } from "@angular/material/card";
import { MatFormFieldModule } from "@angular/material/form-field";
import { MatGridListModule } from "@angular/material/grid-list";
import { MatIconModule } from "@angular/material/icon";
import { MatInputModule } from "@angular/material/input";
import { MatListModule } from "@angular/material/list";
import { MatSelectModule } from "@angular/material/select";
import { MatSidenavModule } from "@angular/material/sidenav";
import { MatToolbarModule } from "@angular/material/toolbar";
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { environment } from "@environments/environment";
import { DatasetToSortedEntriesPipe } from "@pipes/dataset.pipe";
import { BASE_PATH } from "@services/api-client";
import { UserComponent } from "@user/user.component";
import { RECAPTCHA_V3_SITE_KEY, RecaptchaV3Module } from "ng-recaptcha-2";
import { AccordionModule } from "primeng/accordion";
import { AutoCompleteModule } from "primeng/autocomplete";
import { ButtonModule } from "primeng/button";
import { CalendarModule } from "primeng/calendar";
import { ChartModule } from "primeng/chart";
import { CheckboxModule } from "primeng/checkbox";
import { DropdownModule } from "primeng/dropdown";
import { FileUploadModule } from "primeng/fileupload";
import { InputTextModule } from "primeng/inputtext";
import { MenuModule } from "primeng/menu";
import { TableModule } from "primeng/table";
import { ToolbarModule } from "primeng/toolbar";
import { ErrorInterceptor, JwtInterceptor } from "./_helpers";
import { DatePipe } from "./_pipes/date.pipe";
import { DatetimePipe } from "./_pipes/datetime.pipe";
import { StoragePipe } from "./_pipes/storage.pipe";
import { UserInfoToSortedEntriesPipe } from "./_pipes/userInfo.pipe";
import { AccessRequestsComponent } from "./access-requests/access-requests.component";
import { ConfirmationComponent } from "./confirmation/confirmation.component";
import { CountriesComponent } from "./countries/countries.component";
import { DatasetUsersComponent } from "./dataset-users/dataset-users.component";
import { DatasetComponent } from "./dataset/dataset.component";
import { DatasetsComponent } from "./datasets/datasets.component";
import { ForgotPasswordComponent } from "./forgot-password/forgot-password.component";
import { HistoryComponent } from "./history/history.component";
import { HomeComponent } from "./home/home.component";
import { InstitutionsComponent } from "./institutions/institutions.component";
import { LoginComponent } from "./login/login.component";
import { ProfileComponent } from "./profile/profile.component";
import { RegisterComponent } from "./register/register.component";
import { RequestAccessComponent } from "./request-access/request-access.component";
import { ResetPasswordComponent } from "./reset-password/reset-password.component";
import { SccsComponent } from "./sccs/sccs.component";
import { UsersComponent } from "./users/users.component";

@NgModule({
    declarations: [
        AppComponent,
        HomeComponent,
        RegisterComponent,
        LoginComponent,
        ForgotPasswordComponent,
        ResetPasswordComponent,
        ProfileComponent,
        UsersComponent,
        UserComponent,
        CountriesComponent,
        InstitutionsComponent,
        SccsComponent,
        DatasetsComponent,
        DatasetComponent,
        DatasetUsersComponent,
        AccessRequestsComponent,
        HistoryComponent,
        ConfirmationComponent,
        RequestAccessComponent,
        StoragePipe,
        DatePipe,
        DatetimePipe,
        UserInfoToSortedEntriesPipe,
        DatasetToSortedEntriesPipe
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
        RecaptchaV3Module,
        MatFormFieldModule,
        MatInputModule,
        MatGridListModule,
        MatCardModule,
        MatAutocompleteModule,
        MatSelectModule,
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
