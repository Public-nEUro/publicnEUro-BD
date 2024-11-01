export const toBase64 = (file: File): Promise<string> =>
    new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
            if (typeof reader.result === "string") resolve(reader.result);
            else reject();
        };
        reader.onerror = reject;
    });

export const downloadBlob = async (blob: Blob, fileName: string) => {
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(link.href);
};

export const downloadBase64 = async (base64Data: string, fileName: string) => {
    const res = await fetch(base64Data);
    const blob = await res.blob();
    downloadBlob(blob, fileName);
};
