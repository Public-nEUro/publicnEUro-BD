export const downloadFromUrl = (url: string, name: string) => {
    const a = document.createElement("a");
    a.href = url;
    console.log(url);
    a.target = "_blank";
    a.download = name;
    a.click();
    window.URL.revokeObjectURL(a.href);
};
