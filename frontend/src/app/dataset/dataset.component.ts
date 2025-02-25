import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { fieldKeyToLabel } from "@helpers/utils/dataset";
import { downloadBase64, toBase64 } from "@helpers/utils/file";
import { Dataset, DatasetDetails, DefaultService, SccWithId } from "@services/api-client";

@Component({
    selector: "app-dataset",
    templateUrl: "./dataset.component.html",
    styleUrls: ["./dataset.component.scss"]
})
export class DatasetComponent implements OnInit {
    fieldKeyToLabel = fieldKeyToLabel;
    AccessibilityEnum = Dataset.AccessibilityEnum;

    constructor(private router: Router, private route: ActivatedRoute, private service: DefaultService) {}

    accessibilities: Dataset.AccessibilityEnum[] = ["PRIVATE", "EU", "EU_AND_ADEQUATE", "WORLDWIDE", "OPEN"];
    filteredAccessibilities: Dataset.AccessibilityEnum[] = [];

    sccs: SccWithId[] = [];
    filteredSccs: SccWithId[] = [];

    approvalTypes: Dataset.ApprovalTypeEnum[] = ["OVERSIGHT", "AUTOMATED"];
    filteredApprovalTypes: Dataset.ApprovalTypeEnum[] = [];

    dataset: (DatasetDetails & { delphi_share_url?: string }) | null | undefined = undefined;

    editing = false;

    ngOnInit(): void {
        this.refresh();
    }

    getDatasetId() {
        const datasetId = this.route.snapshot.paramMap.get("dataset_id");
        if (datasetId === null) alert("No dataset ID provided");
        return datasetId;
    }

    refresh() {
        const datasetId = this.getDatasetId();
        if (datasetId === null) return;
        this.editing = false;
        this.filteredAccessibilities = this.accessibilities;
        this.filteredSccs = this.sccs;
        this.filteredApprovalTypes = this.approvalTypes;
        this.service.apiGetDatasetPost({ id: datasetId }).subscribe({
            next: res => {
                this.service.apiGetDelphiShareUrlPost({ id: datasetId }).subscribe(({ delphi_share_url }) => {
                    this.dataset = { ...res, delphi_share_url };
                    this.service.apiGetSccsPost({}).subscribe(res => {
                        this.sccs = res.sccs;
                    });
                });
            },
            error: err => {
                if (err.status === 404) this.dataset = null;
                if (err.status === 401)
                    this.router.navigate(["/login"], {
                        queryParams: { redirect: window.location.pathname }
                    });
            }
        });
    }

    onAccessibilityChange(accessibility: string) {
        this.filteredAccessibilities = this.accessibilities.filter(a =>
            a.toLowerCase().includes(accessibility.toLowerCase())
        );
    }

    async onDuaFileSelected(event: Event) {
        if (!this.dataset) return;
        const file = (event.target as HTMLInputElement).files?.[0];
        if (file === undefined) return;
        this.dataset.dua_file_name = file.name;
        this.dataset.dua_file_data = await toBase64(file);
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

    edit() {
        this.editing = true;
        this.filteredAccessibilities = this.accessibilities;
        this.filteredSccs = this.sccs;
        this.filteredApprovalTypes = this.approvalTypes;
    }

    save() {
        if (!this.dataset) return;
        const { scc_file_name, access_info, institution_scc_accepted, ...datasetWithFileData } = this.dataset;
        if (datasetWithFileData.delphi_share_url === undefined) return;
        this.service
            .apiUpdateDatasetPost({ ...datasetWithFileData, delphi_share_url: datasetWithFileData.delphi_share_url })
            .subscribe(() => {
                this.refresh();
            });
    }

    cancel() {
        this.refresh();
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

    gotoDatasetUsers() {
        this.router.navigate([`/admin/datasets/${this.getDatasetId()}/users`]);
    }
}
