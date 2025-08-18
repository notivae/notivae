import { decode, isBlurhashValid } from "blurhash";
import { computed, type MaybeRefOrGetter, toValue } from "vue";

type Options = {
    width: number
    height: number
}

export function useRenderedBlurhash(blurhash: MaybeRefOrGetter<string | undefined | null>, options?: Options) {
    return computed(() => {
        const {
            width = 512,
            height = 512,
        } = options ?? {};

        const bh = toValue(blurhash);
        if (!bh) return null;

        const result = isBlurhashValid(bh)
        if (!result.result) {
            console.error("Invalid blurhash received", { errorReason: result.errorReason, blurhash: bh });
            return null
        }

        const pixels = decode(bh, width, height);

        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d")!;
        const imageData = ctx.createImageData(width, height);
        imageData.data.set(pixels);
        ctx.putImageData(imageData, 0, 0);
        return canvas.toDataURL("image/png");
    })
}
