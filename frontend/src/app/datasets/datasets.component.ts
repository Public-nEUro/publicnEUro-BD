import { Component, OnInit } from "@angular/core";
import { downloadBase64 } from "@helpers/utils/file";
import { Dataset, DefaultService, SccWithId } from "@services/api-client";

@Component({
    selector: "app-datasets",
    templateUrl: "./datasets.component.html",
    styleUrls: ["./datasets.component.scss"]
})
export class DatasetsComponent implements OnInit {
    constructor(private service: DefaultService) {}

    sccs: SccWithId[] = [];

    datasets: Dataset[] = [];

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

    getScc(sccId: string | null) {
        return this.sccs.find(scc => scc.id === sccId);
    }

    getSccTitle(sccId: string) {
        return this.getScc(sccId)?.title ?? "";
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
