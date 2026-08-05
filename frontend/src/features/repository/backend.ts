import {
    repositoryApi,
    type RepositoryUploadRequest,
    type RepositoryUploadResponse,
} from "../api/repository";

export class RepositoryBackend {

    async upload(
        request: RepositoryUploadRequest,
    ): Promise<RepositoryUploadResponse> {

        return repositoryApi.upload(request);

    }

}

export const repositoryBackend =
    new RepositoryBackend();
