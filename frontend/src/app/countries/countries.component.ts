import { Component, OnInit } from "@angular/core";
import { Country, DefaultService } from "@services/api-client";

@Component({
    selector: "app-countries",
    templateUrl: "./countries.component.html",
    styleUrls: ["./countries.component.scss"]
})
export class CountriesComponent implements OnInit {
    constructor(private service: DefaultService) {}

    countries: Country[] = [];

    ngOnInit(): void {
        this.service.apiGetCountriesPost({}).subscribe(res => {
            this.countries = res.countries;
        });
    }
}
