import { Component, OnInit } from "@angular/core";
import { downloadBase64, toBase64 } from "@helpers/utils/file";
import { Dataset, DatasetWithFileData, DefaultService, SccWithId } from "@services/api-client";

@Component({
    selector: "app-datasets",
    templateUrl: "./datasets.component.html",
    styleUrls: ["./datasets.component.scss"]
})
export class DatasetsComponent implements OnInit {
    constructor(private service: DefaultService) {}

    accessibilities: Dataset.AccessibilityEnum[] = ["PRIVATE", "EU", "EU_AND_ADEQUATE", "WORLDWIDE", "PUBLIC"];
    filteredAccessibilities: Dataset.AccessibilityEnum[] = [];

    sccs: SccWithId[] = [];
    filteredSccs: SccWithId[] = [];

    approvalTypes: Dataset.ApprovalTypeEnum[] = ["OVERSIGHT", "AUTOMATED"];
    filteredApprovalTypes: Dataset.ApprovalTypeEnum[] = [];

    datasets: Dataset[] = [];
    editingDataset: DatasetWithFileData | undefined;

    ngOnInit(): void {
        this.reload();
    }

    reload() {
        this.service.apiGetDatasetsPost({}).subscribe(res => {
            this.datasets = res.datasets;
        });
        this.service.apiGetSccsPost({}).subscribe(res => {
            this.sccs = res.sccs;
        });
    }

    edit(dataset: Dataset) {
        this.editingDataset = dataset as DatasetWithFileData;
        this.editingDataset.dua_file_data = null;
        this.filteredAccessibilities = this.accessibilities;
        this.filteredSccs = this.sccs;
        this.filteredApprovalTypes = this.approvalTypes;
    }

    onAccessibilityChange(accessibility: string) {
        this.filteredAccessibilities = this.accessibilities.filter(a =>
            a.toLowerCase().includes(accessibility.toLowerCase())
        );
    }

    async onDuaFileSelected(event: Event) {
        if (this.editingDataset === undefined) return;
        const file = (event.target as HTMLInputElement).files?.[0];
        if (file === undefined) return;
        this.editingDataset.dua_file_name = file.name;
        this.editingDataset.dua_file_data = await toBase64(file);
    }

    onApprovalChange(approvalType: string) {
        this.filteredApprovalTypes = this.approvalTypes.filter(a =>
            a.toLowerCase().includes(approvalType.toLowerCase())
        );
    }

    onSccChange(sccTitle: string) {
        this.filteredSccs = this.sccs.filter(scc => scc.title.toLowerCase().includes(sccTitle.toLowerCase()));
    }

    getScc(sccId: string | null) {
        return this.sccs.find(scc => scc.id === sccId);
    }

    getSccTitle(sccId: string) {
        return this.getScc(sccId)?.title ?? "";
    }

    save(dataset: DatasetWithFileData) {
        this.editingDataset = undefined;
        this.service.apiUpdateDatasetPost(dataset).subscribe(() => {
            this.reload();
        });
    }

    downloadDua(dataset: Dataset) {
        this.service.apiGetDatasetDuaPost({ id: dataset.id }).subscribe(res => {
            downloadBase64(res.file_data, res.file_name);
        });
    }

    downloadScc(dataset: Dataset) {
        if (dataset.scc_id === null) return;
        this.service.apiGetSccPost({ id: dataset.scc_id }).subscribe(res => {
            downloadBase64(res.file_data, res.file_name);
        });
    }
}
