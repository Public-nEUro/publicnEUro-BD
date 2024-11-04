import { Component, OnInit } from "@angular/core";
import { DefaultService, Country, SccWithId, InstitutionWithAcceptance } from "@services/api-client";

type InstitutionWithName = InstitutionWithAcceptance & { country_name: string };

@Component({
    selector: "app-institutions",
    templateUrl: "./institutions.component.html",
    styleUrls: ["./institutions.component.scss"]
})
export class InstitutionsComponent implements OnInit {
    constructor(private service: DefaultService) {}

    countries: Country[] = [];
    filteredCountries: Country[] = [];

    institutions: InstitutionWithName[] = [];
    editingInstitution: InstitutionWithName | undefined;

    sccs: SccWithId[] = [];

    ngOnInit(): void {
        this.service.apiGetCountriesPost({}).subscribe(res => {
            this.countries = res.countries;
            this.reload();
        });
    }

    reload() {
        this.service.apiGetInstitutionsPost({}).subscribe(res2 => {
            this.institutions = res2.institutions.map(i => ({
                ...i,
                country_name: this.countries.find(c => c.id === i.country_id)?.name ?? ""
            }));
        });
        this.service.apiGetSccsPost({}).subscribe(res => {
            this.sccs = res.sccs;
        });
    }

    edit(institution: InstitutionWithName) {
        this.editingInstitution = institution;
        this.onCountryNameChange("");
    }

    onCountryNameChange(name: string) {
        this.filteredCountries = this.countries.filter(country =>
            country.name.toLowerCase().includes(name.toLowerCase())
        );
    }

    save(institutionWithName: InstitutionWithName) {
        const { country_name, ...institution } = institutionWithName;
        institution.country_id = this.countries.find(c => c.name === country_name)?.id ?? null;
        this.editingInstitution = undefined;
        this.service.apiUpdateInstitutionPost(institution).subscribe(() => {
            this.reload();
        });
    }
}
