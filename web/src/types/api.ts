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
