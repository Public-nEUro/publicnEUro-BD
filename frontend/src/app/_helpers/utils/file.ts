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
