import axios from "axios";


export async function postApiLogout() {
    return await axios.post(`/api/auth/logout`);
}
