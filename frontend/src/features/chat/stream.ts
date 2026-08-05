import type { StreamChunk } from "../../contracts";
import { streamBackend } from "../stream/backend";

export interface ChatStream {

    stream(): Promise<StreamChunk>;

}

export class BackendChatStream implements ChatStream {

    async stream(): Promise<StreamChunk> {

        return streamBackend.stream();

    }

}

export const chatStream = new BackendChatStream();
