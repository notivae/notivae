import axios from "axios";
import type { UserMe } from "@/types/api.ts";


export async function getApiMeAccount() {
    return await axios.get<UserMe>("/api/me/account");
}


type AccountChanges = {
    email?: string
    name?: string
    display_name?: string
}


export async function patchApiMeAccount(changes: AccountChanges) {
    return await axios.patch("/api/me/account", changes);
}
