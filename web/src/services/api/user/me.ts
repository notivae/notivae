import axios from "axios";
import type { UserMe } from "@/types/api.ts";


export async function getApiUserMe() {
    return await axios.get<UserMe>("/api/user/me");
}
