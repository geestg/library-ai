import type { StreamChunk } from "../../contracts";

export interface StreamBackend {

    stream(): Promise<StreamChunk>;

}

export class HttpStreamBackend
implements StreamBackend {

    async stream(): Promise<StreamChunk> {

        return {
            id: crypto.randomUUID(),
            type: "token",
            token: "",
            finished: true,
        };

    }

}

export const streamBackend =
    new HttpStreamBackend();
