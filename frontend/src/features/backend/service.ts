import { chatBackend } from "../chat/backend";
import { retrievalBackend } from "../retrieval/backend";
import { repositoryBackend } from "../repository/backend";
import { backendHealth } from "../health/backend";

export class BackendService {

    readonly chat = chatBackend;

    readonly retrieval = retrievalBackend;

    readonly repository = repositoryBackend;

    readonly health = backendHealth;

}

export const backendService =
    new BackendService();
