import axios from "axios"


type LoginParameters = {
    username_or_email: string
    password: string
}

type LoginResponse = {
    success: true
    requires_mfa: boolean
}


export async function postApiAuthLocalLogin(params: LoginParameters) {
    return await axios.post<LoginResponse>("/api/auth/local/login", params);
}
