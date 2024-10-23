import { Component, OnInit } from "@angular/core";
import { Institution, DefaultService, Country } from "@services/api-client";

type InstitutionWithName = Institution & { country_name: string };

@Component({
    selector: "app-institutions",
    templateUrl: "./institutions.component.html",
    styleUrls: ["./institutions.component.scss"]
})
export class InstitutionsComponent implements OnInit {
    constructor(private service: DefaultService) {}

    countries: Country[] = [];
    filteredCountries: Country[] = [];

    sccAcceptances: Institution.SccAcceptanceEnum[] = ["ACCEPT", "DO_NOT_ACCEPT"];
    filteredSccAcceptances: Institution.SccAcceptanceEnum[] = [];

    institutions: InstitutionWithName[] = [];
    editingInstitution: InstitutionWithName | undefined;

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
    }

    edit(institution: InstitutionWithName) {
        this.editingInstitution = institution;
        this.onCountryNameChange("");
        this.onSccAcceptanceChange("");
    }

    onCountryNameChange(name: string) {
        this.filteredCountries = this.countries.filter(country =>
            country.name.toLowerCase().includes(name.toLowerCase())
        );
    }

    onSccAcceptanceChange(name: string) {
        this.filteredSccAcceptances = this.sccAcceptances.filter(sccAcceptance =>
            sccAcceptance.toLowerCase().includes(name.toLowerCase())
        );
    }

    save(institutionWithName: InstitutionWithName) {
        const { country_name, ...institution } = institutionWithName;
        institution.country_id = this.countries.find(c => c.name === country_name)?.id ?? null;
        if (institution.scc_acceptance !== null && !this.sccAcceptances.includes(institution.scc_acceptance))
            institution.scc_acceptance = null;
        this.editingInstitution = undefined;
        this.service.apiUpdateInstitutionPost(institution).subscribe(() => {
            this.reload();
        });
    }
}
