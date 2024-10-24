import { Component, OnInit } from "@angular/core";
import { Dataset, DefaultService, Info } from "@services/api-client";

@Component({
    selector: "app-datasets",
    templateUrl: "./datasets.component.html",
    styleUrls: ["./datasets.component.scss"]
})
export class DatasetsComponent implements OnInit {
    constructor(private service: DefaultService) {}

    accessibilities: Dataset.AccessibilityEnum[] = ["PRIVATE", "EU", "EU_AND_ADEQUATE", "WORLDWIDE", "PUBLIC"];
    filteredAccessibilities: Dataset.AccessibilityEnum[] = [];

    approvalTypes: Info.ApprovalTypeEnum[] = ["OVERSIGHT", "AUTOMATED"];
    filteredDuaApprovalTypes: Info.ApprovalTypeEnum[] = [];
    filteredSccApprovalTypes: Info.ApprovalTypeEnum[] = [];

    datasets: Dataset[] = [];
    editingDataset: Dataset | undefined;

    ngOnInit(): void {
        this.reload();
    }

    reload() {
        this.service.apiGetDatasetsPost({}).subscribe(res => {
            this.datasets = res.datasets;
        });
    }

    edit(dataset: Dataset) {
        this.editingDataset = dataset;
        this.filteredAccessibilities = this.accessibilities;
        this.filteredDuaApprovalTypes = this.approvalTypes;
        this.filteredSccApprovalTypes = this.approvalTypes;
    }

    onAccessibilityChange(accessibility: string) {
        this.filteredAccessibilities = this.accessibilities.filter(a =>
            a.toLowerCase().includes(accessibility.toLowerCase())
        );
    }

    onDuaApprovalChange(approvalType: string) {
        this.filteredDuaApprovalTypes = this.approvalTypes.filter(a =>
            a.toLowerCase().includes(approvalType.toLowerCase())
        );
    }

    onSccApprovalChange(approvalType: string) {
        this.filteredSccApprovalTypes = this.approvalTypes.filter(a =>
            a.toLowerCase().includes(approvalType.toLowerCase())
        );
    }

    save(dataset: Dataset) {
        this.editingDataset = undefined;
        this.service.apiUpdateDatasetPost(dataset).subscribe(() => {
            this.reload();
        });
    }
}
