export class StubStreamClient {
    async stream() {
        return {
            id: crypto.randomUUID(),
            type: "token",
            token: "",
            finished: true,
        };
    }
}
export const streamClient = new StubStreamClient();
