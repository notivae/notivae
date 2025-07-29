import axios from "axios"


type RegisterParameters = {
    username: string
    display_name: string
    password: string
    email: string
}


export async function postApiAuthLocalRegister(params: RegisterParameters) {
    return await axios.post("/api/auth/local/register", params);
}
