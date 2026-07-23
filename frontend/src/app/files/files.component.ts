import { CommonModule } from "@angular/common";
import { Component, inject, OnInit } from "@angular/core";
import { ActivatedRoute } from "@angular/router";
import { downloadFromUrl } from "@helpers/utils/download";
import { DefaultService } from "@services/api-client";
import { TreeNode } from "primeng/api";
import { ButtonModule } from "primeng/button";
import { TreeModule, TreeNodeExpandEvent } from "primeng/tree";
import { firstValueFrom } from "rxjs";

const isParentDir = (a: string, b: string): boolean => b.substring(0, a.length) === a;

@Component({
    selector: "app-files",
    standalone: true,
    imports: [CommonModule, TreeModule, ButtonModule],
    templateUrl: "./files.component.html"
})
export class FilesComponent implements OnInit {
    private route = inject(ActivatedRoute);
    private service = inject(DefaultService);

    datasetId?: string;

    files: TreeNode[] = [];

    async ngOnInit() {
        this.files = await this.loadChildren("");
    }

    async getSharedKey() {
        const params = await firstValueFrom(this.route.paramMap);
        const dataset_id = params.get("dataset_id") ?? null;
        if (dataset_id === null) throw new Error("No dataset ID provided");
        this.datasetId = dataset_id;
        const shared_key = params.get("shared_key") ?? null;
        if (shared_key === null) throw new Error("No key provided");
        return shared_key;
    }

    async getFiles(path: string) {
        const shared_key = await this.getSharedKey();
        const res = await firstValueFrom(this.service.apiListFilesPost({ share_auth: shared_key, path }));
        return res.files;
    }

    selectedNodes: TreeNode[] = [];

    async onExpand(event: TreeNodeExpandEvent): Promise<void> {
        const node = event.node;
        node.expanded = true;

        if (node.children) return;

        node.loading = true;
        try {
            node.children = await this.loadChildren(node.key ?? "");
        } finally {
            node.loading = false;
        }
    }

    async loadChildren(folderId: string): Promise<TreeNode[]> {
        return (await this.getFiles(folderId)).map(file => {
            return {
                key: file.path,
                label: file.name,
                type: file.type === "-" ? "file" : "folder",
                leaf: file.type === "-"
            };
        });
    }

    async download(selectedNodes: TreeNode[]) {
        const rawPaths = selectedNodes.map(n => n.key).filter(key => key !== undefined);
        const paths = rawPaths.filter(path => !rawPaths.some(p => p !== path && isParentDir(p, path)));
        const res = await firstValueFrom(
            this.service.apiPrepareZipPost({
                share_auth: await this.getSharedKey(),
                paths
            })
        );
        downloadFromUrl(res.url, "qwe.zip");
    }
}
