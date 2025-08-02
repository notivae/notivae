import axios from "axios"


type ForgotPasswordParameters = {
    email: string
}


export async function postApiAuthLocalForgotPassword(params: ForgotPasswordParameters) {
    return await axios.post<void>("/api/auth/local/forgot-password", params);
}
