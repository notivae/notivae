import axios from "axios";


export async function postApiAuthMagicUnlink() {
    return axios.post('/api/auth/magic/unlink');
}
