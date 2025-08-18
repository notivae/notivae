import axios from "axios";

export async function putApiUsersAvatar(userId: string, imageBlob: Blob) {
    const form = new FormData();
    form.append("file", imageBlob);
    return await axios.put<void>(`/api/users/${userId}/avatar`, form);
}

export async function deleteApiUsersAvatar(userId: string) {
    return await axios.delete<void>(`/api/users/${encodeURIComponent(userId)}/avatar`);
}
