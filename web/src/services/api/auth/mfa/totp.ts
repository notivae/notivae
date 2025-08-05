import axios from "axios";
import type { MfaTotpInit } from "@/types/api.ts";


type TotpConfirmParams = {
    otp: string
}


export async function postApiAuthMFATotpConfirm(params: TotpConfirmParams) {
    return await axios.post<void>("/api/auth/mfa/totp/confirm", params)
}


export async function postApiAuthMFATotpInit() {
    return await axios.post<MfaTotpInit>("/api/auth/mfa/totp/init")
}

export async function deleteApiAuthMFATotp() {
    return await axios.delete<void>("/api/auth/mfa/totp");
}


type TotpVerifyParams = {
    otp: string
}


export async function postApiAuthMFATotpVerify(params: TotpVerifyParams) {
    return await axios.post<void>("/api/auth/mfa/totp/verify", params)
}
