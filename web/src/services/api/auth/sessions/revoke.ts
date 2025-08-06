import axios from "axios";


type RevokeParams = {
    session_ids: number[]
}


export async function postApiAuthSessionsRevoke(params: RevokeParams) {
    return await axios.post<void>("/api/auth/sessions/revoke", params);
}
