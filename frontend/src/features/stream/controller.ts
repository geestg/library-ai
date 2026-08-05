import type { StreamChunk } from "../../contracts";
import { streamBackend } from "./backend";

export type StreamListener =
    (chunk: StreamChunk) => void;

export class StreamController {

    async start(
        listener?: StreamListener,
    ): Promise<StreamChunk> {

        const chunk =
            await streamBackend.stream();

        listener?.(chunk);

        return chunk;

    }

}

export const streamController =
    new StreamController();
