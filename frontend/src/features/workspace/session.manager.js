import { workspaceFacade } from "./facade";
import { workspacePersistence } from "./persistence";
export class WorkspaceSessionManager {
    initialize() {
        const snapshot = workspacePersistence.load();
        if (!snapshot) {
            return;
        }
        workspaceFacade.setMessages(snapshot.messages);
    }
    persist() {
        workspacePersistence.save({
            messages: workspaceFacade.messages,
        });
    }
    reset() {
        workspaceFacade.reset();
        workspacePersistence.save({
            messages: [],
        });
    }
}
export const workspaceSessionManager = new WorkspaceSessionManager();
