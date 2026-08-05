import { repositoryBackend, } from "./backend";
export class BackendRepositoryIndexer {
    async index(request) {
        await repositoryBackend.upload({
            files: request.files,
        });
        return {
            queued: true,
        };
    }
}
export const repositoryIndexer = new BackendRepositoryIndexer();
