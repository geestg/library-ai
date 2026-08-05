import { create } from "zustand";

import type { RepositoryDocument } from "../types/repository";

export interface WorkspaceMessage {

    id: string;

    role:
        | "user"
        | "assistant";

    content: string;

    createdAt: number;
}

interface WorkspaceState {

    workspaceId: string;

    title: string;

    messages: WorkspaceMessage[];

    citations: RepositoryDocument[];

    loading: boolean;

    streaming: boolean;

    setWorkspace(
        id: string,
        title: string,
    ): void;

    setMessages(
        messages: WorkspaceMessage[],
    ): void;

    addMessage(
        message: WorkspaceMessage,
    ): void;

    setLoading(
        loading: boolean,
    ): void;

    setStreaming(
        streaming: boolean,
    ): void;

    setCitations(
        citations: RepositoryDocument[],
    ): void;

    reset(): void;
}

export const useWorkspaceStore =
create<WorkspaceState>((set) => ({

    workspaceId: "",

    title: "Untitled Workspace",

    messages: [],

    citations: [],

    loading: false,

    streaming: false,

    setWorkspace: (id, title) =>
        set({
            workspaceId: id,
            title,
        }),

    setMessages: (messages) =>
        set({
            messages,
        }),

    addMessage: (message) =>
        set((state) => ({
            messages: [
                ...state.messages,
                message,
            ],
        })),

    setLoading: (loading) =>
        set({
            loading,
        }),

    setStreaming: (streaming) =>
        set({
            streaming,
        }),

    setCitations: (citations) =>
        set({
            citations,
        }),

    reset: () =>
        set({

            workspaceId: "",

            title: "Untitled Workspace",

            messages: [],

            citations: [],

            loading: false,

            streaming: false,

        }),

}));
