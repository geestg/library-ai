import type { WorkspaceMessage } from "../../stores/workspace.store";

const STORAGE_KEY = "delbot.workspace";

export interface WorkspaceSnapshot {
    messages: WorkspaceMessage[];
}

export class WorkspacePersistence {

    load(): WorkspaceSnapshot {

        try {

            const raw = localStorage.getItem(STORAGE_KEY);

            if (!raw) {
                return {
                    messages: [],
                };
            }

            return JSON.parse(raw) as WorkspaceSnapshot;

        } catch {

            return {
                messages: [],
            };

        }

    }

    save(snapshot: WorkspaceSnapshot): void {

        localStorage.setItem(
            STORAGE_KEY,
            JSON.stringify(snapshot),
        );

    }

    clear(): void {

        localStorage.removeItem(STORAGE_KEY);

    }

}

export const workspacePersistence =
    new WorkspacePersistence();
