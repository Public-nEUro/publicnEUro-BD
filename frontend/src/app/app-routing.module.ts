import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";
import { HomeComponent } from "./home/home.component";
import { RegisterComponent } from "./register/register.component";
import { LoginComponent } from "./login/login.component";
import { ProfileComponent } from "./profile/profile.component";
import { UsersComponent } from "./users/users.component";
import { UserComponent } from "@user/user.component";
import { CountriesComponent } from "./countries/countries.component";
import { ConfirmationComponent } from "./confirmation/confirmation.component";
import { InstitutionsComponent } from "./institutions/institutions.component";
import { SccsComponent } from "./sccs/sccs.component";
import { DatasetsComponent } from "./datasets/datasets.component";
import { DatasetComponent } from "./dataset/dataset.component";
import { HistoryComponent } from "./history/history.component";
import { RequestAccessComponent } from "./request-access/request-access.component";
import { AccessRequestsComponent } from "./access-requests/access-requests.component";
import { DatasetUsersComponent } from "./dataset-users/dataset-users.component";
import { ForgotPasswordComponent } from "./forgot-password/forgot-password.component";
import { ResetPasswordComponent } from "./reset-password/reset-password.component";

const routes: Routes = [
    {
        path: "",
        component: HomeComponent
    },
    {
        path: "register",
        component: RegisterComponent
    },
    {
        path: "login",
        component: LoginComponent
    },
    {
        path: "forgot_password",
        component: ForgotPasswordComponent
    },
    {
        path: "reset_password/:email_confirmation_passkey",
        component: ResetPasswordComponent
    },
    {
        path: "profile",
        component: ProfileComponent
    },
    {
        path: "admin/users",
        component: UsersComponent
    },
    {
        path: "admin/users/:user_id",
        component: UserComponent
    },
    {
        path: "admin/countries",
        component: CountriesComponent
    },
    {
        path: "admin/institutions",
        component: InstitutionsComponent
    },
    {
        path: "admin/sccs",
        component: SccsComponent
    },
    {
        path: "admin/datasets",
        component: DatasetsComponent
    },
    {
        path: "admin/datasets/:dataset_id",
        component: DatasetComponent
    },
    {
        path: "admin/datasets/:dataset_id/users",
        component: DatasetUsersComponent
    },
    {
        path: "admin/access-requests",
        component: AccessRequestsComponent
    },
    {
        path: "admin/history",
        component: HistoryComponent
    },
    {
        path: "confirmation/:email_confirmation_passkey",
        component: ConfirmationComponent
    },
    {
        path: "request-access/:dataset_id",
        component: RequestAccessComponent
    }
];

@NgModule({
    declarations: [],
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule {}
