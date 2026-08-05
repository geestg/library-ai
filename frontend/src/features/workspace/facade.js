import { useWorkspaceStore } from "../../stores/workspace.store";
export class WorkspaceFacade {
    get state() {
        return useWorkspaceStore.getState();
    }
    get messages() {
        return this.state.messages;
    }
    addMessage = this.state.addMessage;
    setMessages = this.state.setMessages;
    reset() {
        this.state.setMessages([]);
    }
}
export const workspaceFacade = new WorkspaceFacade();
