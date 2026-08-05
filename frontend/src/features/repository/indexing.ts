import {
    repositoryBackend,
} from "./backend";

export interface RepositoryIndexRequest {
    files: File[];
}

export interface RepositoryIndexResponse {
    queued: boolean;
}

export interface RepositoryIndexer {
    index(
        request: RepositoryIndexRequest,
    ): Promise<RepositoryIndexResponse>;
}

export class BackendRepositoryIndexer
implements RepositoryIndexer {

    async index(
        request: RepositoryIndexRequest,
    ): Promise<RepositoryIndexResponse> {

        await repositoryBackend.upload({
            files: request.files,
        });

        return {
            queued: true,
        };
    }

}

export const repositoryIndexer =
    new BackendRepositoryIndexer();
