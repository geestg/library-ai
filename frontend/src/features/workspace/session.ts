import { workspaceFacade } from "./facade";
import {
    workspacePersistence,
    type WorkspaceSnapshot,
} from "./persistence";

export class WorkspaceSession {

    load(): WorkspaceSnapshot | null {

        const snapshot =
            workspacePersistence.load();

        if (snapshot) {
            workspaceFacade.setMessages(
                snapshot.messages,
            );
        }

        return snapshot;
    }

    save() {

        workspacePersistence.save({
            messages:
                workspaceFacade.messages,
        });

    }

    reset() {

        workspaceFacade.reset();

        workspacePersistence.save({
            messages: [],
        });

    }

}

export const workspaceSession =
    new WorkspaceSession();
