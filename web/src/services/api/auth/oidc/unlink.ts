import axios from "axios";


export async function postApiAuthOIDCUnlink() {
    return await axios.post<void>("/api/auth/oidc/unlink");
}
