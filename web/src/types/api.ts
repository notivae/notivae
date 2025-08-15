export type ServerAuthFeatures = {
    local: boolean
    oidc: boolean
    magic_link: boolean
}

export type ServerServices = {
    mail: boolean
    virus_scanning: boolean
}

export type AccountCreationMode = "closed" | "restricted" | "open"

export type ServerFeatures = {
    auth: ServerAuthFeatures
    services: ServerServices
    account_creation: AccountCreationMode
}


export type User = {
    id: string
    name: string
    display_name?: string
}

export type UserMe = User & {
    email: string
    email_verified: boolean
    is_system_admin: boolean
}

export type UserInfo = {
    sub: string | null
    nickname: string | null
    preferred_username: string | null
    email: string
    email_verified: boolean | null
    picture: string | null
    locale: string | null
}

export type AuthIdentity = {
    provider: string
    provider_user_id: string
    provider_email: string
    userinfo: null | UserInfo
}


export type BackupCodes = string[]


export type MfaDetails = {
    backup_codes_remaining: null | number
    totp: boolean
}

export type MfaTotpInit = {
    secret: string
    provisioning_uri: string
}

export type AuthSessionInfo = {
    id: number
    is_current: boolean

    user_agent: string
    ip_address: string

    created_at: string
    expires_at: string
    revoked: boolean
}


export type AdminLogMessage = {
    level: number
    module: string
    lineno: number
    message: string
    context: Record<string, unknown>
    timestamp: string
}
