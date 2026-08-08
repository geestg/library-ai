const BASE_URL = import.meta.env.VITE_API_URL ??
    "";
export class ApiClient {
    async get(url) {
        const response = await fetch(BASE_URL + url);
        if (!response.ok) {
            throw new Error(`GET ${url} : ${response.status}`);
        }
        return response.json();
    }
    async post(url, body) {
        const response = await fetch(BASE_URL + url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: body === undefined
                ? undefined
                : JSON.stringify(body),
        });
        if (!response.ok) {
            throw new Error(`POST ${url} : ${response.status}`);
        }
        return response.json();
    }
}
export const apiClient = new ApiClient();
