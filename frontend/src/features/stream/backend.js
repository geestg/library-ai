export class HttpStreamBackend {
    async stream() {
        return {
            id: crypto.randomUUID(),
            type: "token",
            token: "",
            finished: true,
        };
    }
}
export const streamBackend = new HttpStreamBackend();
