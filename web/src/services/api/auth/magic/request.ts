import axios from "axios";

type MagicRequestParameters = {
    email: string
}

export async function postApiAuthMagicRequest(params: MagicRequestParameters) {
    return axios.post('/api/auth/magic/request', params);
}
