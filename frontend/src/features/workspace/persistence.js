const STORAGE_KEY = "delbot.workspace";
export class WorkspacePersistence {
    load() {
        try {
            const raw = localStorage.getItem(STORAGE_KEY);
            if (!raw) {
                return {
                    messages: [],
                };
            }
            return JSON.parse(raw);
        }
        catch {
            return {
                messages: [],
            };
        }
    }
    save(snapshot) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(snapshot));
    }
    clear() {
        localStorage.removeItem(STORAGE_KEY);
    }
}
export const workspacePersistence = new WorkspacePersistence();
