import {
    repositorySearcher,
    type RepositorySearchRequest,
} from "./search";

export class RepositorySynchronization {

    async search(
        request: RepositorySearchRequest,
    ) {
        return repositorySearcher.search(request);
    }

    async sync(
        request: RepositorySearchRequest,
    ) {
        return this.search(request);
    }

}

export const repositorySynchronization =
    new RepositorySynchronization();
