import { Component, OnInit } from "@angular/core";
import { Institution, DefaultService } from "@services/api-client";

@Component({
    selector: "app-institutions",
    templateUrl: "./institutions.component.html",
    styleUrls: ["./institutions.component.scss"]
})
export class InstitutionsComponent implements OnInit {
    constructor(private service: DefaultService) {}

    institutions: Institution[] = [];

    ngOnInit(): void {
        this.reload();
    }

    reload() {
        this.service.apiGetInstitutionsPost({}).subscribe(res => {
            this.institutions = res.institutions;
        });
    }
}
