import axios from "axios";
import type { MfaDetails } from "@/types/api.ts";


export async function getApiMeAuthMfaDetails() {
    return await axios.get<MfaDetails>("/api/me/mfa-details");
}
