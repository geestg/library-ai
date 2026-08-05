import { streamBackend } from "../stream/backend";
export class BackendChatStream {
    async stream() {
        return streamBackend.stream();
    }
}
export const chatStream = new BackendChatStream();
