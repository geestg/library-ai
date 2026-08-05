import { chatBackend } from "../chat/backend";
import { retrievalBackend } from "../retrieval/backend";
import { repositoryBackend } from "../repository/backend";
import { backendHealth } from "../health/backend";
export class BackendService {
    chat = chatBackend;
    retrieval = retrievalBackend;
    repository = repositoryBackend;
    health = backendHealth;
}
export const backendService = new BackendService();
