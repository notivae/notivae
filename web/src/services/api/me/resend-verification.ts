import axios from "axios";

export async function postApiMeResendVerification() {
    return await axios.post<void>("/api/me/resend-verification");
}
