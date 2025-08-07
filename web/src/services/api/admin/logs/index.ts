import axios from "axios";
import type { AdminLogMessage } from "@/types/api.ts";

export async function getApiAdminLogs() {
    return axios.get<AdminLogMessage[]>("/api/admin/logs");
}
