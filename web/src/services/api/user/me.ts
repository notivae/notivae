import axios from "axios";
import type { UserMe } from "@/types/api.ts";


export async function getApiUserMe() {
    return await axios.get<UserMe>("/api/user/me");
}


type UserMeChanges = {
    email?: string
    name?: string
    display_name?: string
}


export async function patchApiUserMe(changes: UserMeChanges) {
    return await axios.patch("/api/user/me", changes);
}
