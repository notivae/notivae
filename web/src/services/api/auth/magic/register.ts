import axios from "axios";

type MagicRegisterParameters = {
    new_user?: {
        username: string
        display_name: string
    }
    email: string
}

export async function postApiAuthMagicRegister(params: MagicRegisterParameters) {
    return axios.post('/api/auth/magic/register', params);
}
