import {
    repositorySynchronization,
} from "./synchronization";

import type {
    RepositorySearchRequest,
} from "./search";

export class RepositoryFlow {

    async search(
        request: RepositorySearchRequest,
    ) {
        return repositorySynchronization.sync(request);
    }

}

export const repositoryFlow =
    new RepositoryFlow();
