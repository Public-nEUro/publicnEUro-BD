import { Component, OnInit } from "@angular/core";
import { Institution, DefaultService } from "@services/api-client";

type InstitutionWithName = Institution & { country_name: string };

@Component({
    selector: "app-institutions",
    templateUrl: "./institutions.component.html",
    styleUrls: ["./institutions.component.scss"]
})
export class InstitutionsComponent implements OnInit {
    constructor(private service: DefaultService) {}

    institutions: InstitutionWithName[] = [];

    ngOnInit(): void {
        this.reload();
    }

    reload() {
        this.service.apiGetCountriesPost({}).subscribe(res1 => {
            this.service.apiGetInstitutionsPost({}).subscribe(res2 => {
                this.institutions = res2.institutions.map(i => ({
                    ...i,
                    country_name: res1.countries.find(c => c.id === i.country_id)?.name ?? ""
                }));
            });
        });
    }
}
