import axios from "axios";


export async function postApiAuthLocalUnlink() {
    return await axios.post<void>("/api/auth/local/unlink");
}
