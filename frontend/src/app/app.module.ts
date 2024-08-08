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
import { ErrorInterceptor, JwtInterceptor } from "./_helpers";
import { CommonModule } from "@angular/common";
import { HomeComponent } from "./home/home.component";
import { LoginComponent } from "./login/login.component";
import { BASE_PATH } from "@services/api-client";
import { environment } from "@environments/environment";

@NgModule({
    declarations: [AppComponent, HomeComponent, LoginComponent, StoragePipe, DatePipe, DatetimePipe],
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
        FileUploadModule
    ],
    providers: [
        { provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true },
        { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },
        { provide: BASE_PATH, useValue: environment.API_BASE_URL }
    ],
    bootstrap: [AppComponent]
})
export class AppModule {}
