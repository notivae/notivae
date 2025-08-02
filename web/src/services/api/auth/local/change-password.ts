import axios from "axios"


type ChangePasswordParameters = {
    new_password: string
    token?: string
}


export async function postApiAuthLocalChangePassword(params: ChangePasswordParameters) {
    return await axios.post("/api/auth/local/change-password", params);
}
