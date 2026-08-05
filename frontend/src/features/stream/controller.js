import { streamBackend } from "./backend";
export class StreamController {
    async start(listener) {
        const chunk = await streamBackend.stream();
        listener?.(chunk);
        return chunk;
    }
}
export const streamController = new StreamController();
