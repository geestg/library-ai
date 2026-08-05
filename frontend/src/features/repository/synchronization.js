import { repositorySearcher, } from "./search";
export class RepositorySynchronization {
    async search(request) {
        return repositorySearcher.search(request);
    }
    async sync(request) {
        return this.search(request);
    }
}
export const repositorySynchronization = new RepositorySynchronization();
