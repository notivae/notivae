export type WebSocketIncomingEvents = {
    notification: Notification
}

export type WebSocketOutgoingEvents = {

}


export type NotificationStatus = "unread" | "read" | "archived"

export type Notification = {
    /** unique identifier for a notification */
    id: number

    /** notification title */
    title: string
    /** notification message */
    message: string

    /** notification category */
    category: string
    /** notification status. See {@link NotificationStatus} */
    status: NotificationStatus

    /** datetime where the message was created */
    created_at: string
    /** optional datetime where this message will no longer be relevant */
    expires_at: string

    /** optional contextual information. depends on {@link category} */
    context: null | object
}
