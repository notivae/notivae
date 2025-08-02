import axios from "axios";
import type { AuthIdentity } from "@/types/api.ts";


export async function getApiUserAuthIdentities() {
    return await axios.get<AuthIdentity[]>("/api/user/auth-identities");
}
