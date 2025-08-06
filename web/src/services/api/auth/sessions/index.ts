import axios from "axios";
import type { AuthSessionInfo } from "@/types/api.ts";

export async function getApiAuthSessions() {
    return await axios.get<AuthSessionInfo[]>("/api/auth/sessions");
}
