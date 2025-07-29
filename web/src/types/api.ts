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
    display_name: string
}

export type UserMe = User & {
    email: string
    email_verified: boolean
    is_system_admin: boolean
}
