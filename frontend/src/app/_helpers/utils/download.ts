export const downloadFromUrl = (url: string) => {
    const a = document.createElement("a");
    a.href = url;
    console.log(url);
    a.target = "_blank";
    a.click();
    window.URL.revokeObjectURL(a.href);
};
