import { repositoryApi, } from "../api/repository";
export class RepositoryBackend {
    async upload(request) {
        return repositoryApi.upload(request);
    }
}
export const repositoryBackend = new RepositoryBackend();
