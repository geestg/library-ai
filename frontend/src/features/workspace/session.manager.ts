import { workspaceFacade } from "./facade";
import { workspacePersistence } from "./persistence";

export class WorkspaceSessionManager {

    initialize(): void {

        const snapshot = workspacePersistence.load();

        if (!snapshot) {
            return;
        }

        workspaceFacade.setMessages(snapshot.messages);

    }

    persist(): void {

        workspacePersistence.save({
            messages: workspaceFacade.messages,
        });

    }

    reset(): void {

        workspaceFacade.reset();

        workspacePersistence.save({
            messages: [],
        });

    }

}

export const workspaceSessionManager =
    new WorkspaceSessionManager();
