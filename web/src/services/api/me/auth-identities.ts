import axios from "axios";
import type { AuthIdentity } from "@/types/api.ts";


export async function getApiMeAuthIdentities() {
    return await axios.get<AuthIdentity[]>("/api/me/auth-identities");
}
