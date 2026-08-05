import type { StreamChunk } from "../../contracts";

export interface StreamClient {
    stream(): Promise<StreamChunk>;
}

export class StubStreamClient implements StreamClient {

    async stream(): Promise<StreamChunk> {

        return {
            id: crypto.randomUUID(),
            type: "token",
            token: "",
            finished: true,
        };

    }

}

export const streamClient = new StubStreamClient();
