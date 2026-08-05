import { create } from "zustand";
export const useWorkspaceStore = create((set) => ({
    workspaceId: "",
    title: "Untitled Workspace",
    messages: [],
    citations: [],
    loading: false,
    streaming: false,
    setWorkspace: (id, title) => set({
        workspaceId: id,
        title,
    }),
    setMessages: (messages) => set({
        messages,
    }),
    addMessage: (message) => set((state) => ({
        messages: [
            ...state.messages,
            message,
        ],
    })),
    setLoading: (loading) => set({
        loading,
    }),
    setStreaming: (streaming) => set({
        streaming,
    }),
    setCitations: (citations) => set({
        citations,
    }),
    reset: () => set({
        workspaceId: "",
        title: "Untitled Workspace",
        messages: [],
        citations: [],
        loading: false,
        streaming: false,
    }),
}));
