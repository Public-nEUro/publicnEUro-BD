import { Component, OnInit } from "@angular/core";
import { UntypedFormControl, UntypedFormGroup } from "@angular/forms";
import { Country, DefaultService } from "@services/api-client";
import { map, Observable, startWith } from "rxjs";

@Component({
    selector: "app-countries",
    templateUrl: "./countries.component.html",
    styleUrls: ["./countries.component.scss"]
})
export class CountriesComponent implements OnInit {
    constructor(private service: DefaultService) {}

    addCountryForm: UntypedFormGroup = new UntypedFormGroup({
        name: new UntypedFormControl(""),
        geo_location: new UntypedFormControl("")
    });

    geoLocations: Country.GeoLocationEnum[] = ["EU", "ADEQUATE", "OTHER"];
    filteredGeoLocations!: Observable<Country.GeoLocationEnum[]>;

    countries: Country[] = [];

    ngOnInit(): void {
        this.reload();
    }

    reload() {
        this.addCountryForm.reset();
        this.service.apiGetCountriesPost({}).subscribe(res => {
            this.countries = res.countries;
        });
        this.filteredGeoLocations = this.addCountryForm.get("geo_location")!.valueChanges.pipe(
            startWith(""),
            map((value: string) =>
                this.geoLocations.filter(geoLocation => geoLocation.toLowerCase().includes(value.toLowerCase()))
            )
        );
    }

    get f() {
        return this.addCountryForm.controls;
    }

    addCountry() {
        this.service
            .apiAddCountryPost({
                name: this.f["name"].value,
                geo_location: this.f["geo_location"].value
            })
            .subscribe(() => {
                this.reload();
            });
    }

    deleteCountry(country: Country) {
        if (!window.confirm(`You are about to delete "${country.name}". Are you sure?`)) return;
        this.service
            .apiDeleteCountryPost({
                id: country.id
            })
            .subscribe(() => {
                this.reload();
            });
    }
}
