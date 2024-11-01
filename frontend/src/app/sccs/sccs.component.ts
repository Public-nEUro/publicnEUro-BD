import { Component, OnInit } from "@angular/core";
import { FormControl, UntypedFormControl, UntypedFormGroup } from "@angular/forms";
import { downloadBase64 } from "@helpers/utils/file";
import { Scc, DefaultService } from "@services/api-client";

const toBase64 = (file: File): Promise<string> =>
    new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
            if (typeof reader.result === "string") resolve(reader.result);
            else reject();
        };
        reader.onerror = reject;
    });

@Component({
    selector: "app-sccs",
    templateUrl: "./sccs.component.html",
    styleUrls: ["./sccs.component.scss"]
})
export class SccsComponent implements OnInit {
    constructor(private service: DefaultService) {}

    addSccForm: UntypedFormGroup = new UntypedFormGroup({
        title: new UntypedFormControl(""),
        file: new FormControl(null)
    });
    file?: File;

    sccs: Scc[] = [];

    ngOnInit(): void {
        this.reload();
    }

    reload() {
        this.addSccForm.reset();
        this.service.apiGetSccsPost({}).subscribe(res => {
            this.sccs = res.sccs;
        });
    }

    onFileSelected(event: Event) {
        const file = (event.target as HTMLInputElement).files?.[0];
        if (file === undefined) return;
        this.file = file;
    }

    get f() {
        return this.addSccForm.controls;
    }

    async addScc() {
        if (this.file === undefined) {
            alert("Please select a file");
            return;
        }
        this.service
            .apiAddSccPost({
                title: this.f["title"].value,
                file_name: this.file.name,
                file_data: await toBase64(this.file)
            })
            .subscribe(() => {
                this.reload();
            });
    }

    downloadScc(id: string) {
        const scc = this.sccs.find(scc => scc.id === id);
        if (scc === undefined) return;
        downloadBase64(scc.file_data, scc.file_name);
    }
}
