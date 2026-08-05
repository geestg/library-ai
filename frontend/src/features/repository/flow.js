import { repositorySynchronization, } from "./synchronization";
export class RepositoryFlow {
    async search(request) {
        return repositorySynchronization.sync(request);
    }
}
export const repositoryFlow = new RepositoryFlow();
