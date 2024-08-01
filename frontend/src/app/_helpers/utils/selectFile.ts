export const selectFile = (): Promise<Blob> => {
    return new Promise(resolve => {
        const input = document.createElement("input");
        input.type = "file";

        input.onchange = (e: Event) => {
            const target = e.target as HTMLInputElement | null;
            if (target === null) return;
            const files = target.files;
            if (files === null) return;
            const file = files[0];
            resolve(file);
        };

        input.click();
    });
};
