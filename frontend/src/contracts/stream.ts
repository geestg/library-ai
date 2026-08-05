export interface StreamChunk {

    id: string;

    type:
        | "start"
        | "token"
        | "citation"
        | "done"
        | "error";

    token?: string;

    message?: string;

    finished?: boolean;
}
