type Options = {
    accept: string
}

export async function pickFile(options?: Options) {
    const {
        accept = '*/*',
    } = options ?? {};

    return new Promise<File>((resolve, reject) => {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = accept;

        input.onchange = () => {
            const file = input.files![0];
            if (file) {
                resolve(file);
            } else {
                reject(new Error("canceled"));
            }
        };

        input.click();
    })
}
