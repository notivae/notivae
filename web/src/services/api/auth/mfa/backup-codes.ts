import axios from "axios";
import type { BackupCodes } from "@/types/api.ts";


type MfaBackupRegenerateResponse = {
    backup_codes: BackupCodes
}


export async function postApiAuthMfaBackupRegenerate() {
    return await axios.post<MfaBackupRegenerateResponse>("/api/auth/mfa/backup/regenerate");
}


type VerifyParams = {
    backup_code: string
}


export async function postApiAuthMfaBackupVerify(params: VerifyParams) {
    return await axios.post<void>("/api/auth/mfa/backup/verify", params);
}
