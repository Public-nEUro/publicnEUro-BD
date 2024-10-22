import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";
import { HomeComponent } from "./home/home.component";
import { RegisterComponent } from "./register/register.component";
import { LoginComponent } from "./login/login.component";
import { ProfileComponent } from "./profile/profile.component";
import { UsersComponent } from "./users/users.component";
import { CountriesComponent } from "./countries/countries.component";
import { ConfirmationComponent } from "./confirmation/confirmation.component";
import { ApprovalComponent } from "./approval/approval.component";

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
        path: "profile",
        component: ProfileComponent
    },
    {
        path: "users",
        component: UsersComponent
    },
    {
        path: "countries",
        component: CountriesComponent
    },
    {
        path: "confirmation/:email_confirmation_passkey",
        component: ConfirmationComponent
    },
    {
        path: "approval/:approver_passkey",
        component: ApprovalComponent
    }
];

@NgModule({
    declarations: [],
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule {}
