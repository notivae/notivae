export function browserDownloadStringAsFile(content: string, filename: string) {
    const blob = new Blob([content], { type: "text/plain" });

    // Start download
    const anchor = document.createElement("a");
    anchor.href = URL.createObjectURL(blob);
    anchor.download = filename;
    document.body.appendChild(anchor);
    anchor.click();

    // Clean up
    document.body.removeChild(anchor);
    URL.revokeObjectURL(anchor.href);
}
