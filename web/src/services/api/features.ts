import axios from "axios";
import type { ServerFeatures } from "@/types/api.ts";


export async function getApiFeatures() {
    return await axios.get<ServerFeatures>("/api/features");
}
