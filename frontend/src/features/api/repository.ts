import { apiClient } from "./client";

export interface RepositoryUploadRequest {
    files: File[];
}

export interface RepositoryUploadResponse {
    accepted: number;
}

export class RepositoryApi {

    async upload(
        request: RepositoryUploadRequest,
    ): Promise<RepositoryUploadResponse> {

        /*
         * MVP NOTE
         *
         * Backend upload endpoint belum selesai.
         * Tetap gunakan canonical ApiClient agar
         * contract frontend sudah benar.
         */

        void apiClient;

        return {
            accepted: request.files.length,
        };

        /*
        Sprint 815
        return apiClient.post<RepositoryUploadResponse>(
            "/repository/upload",
            request,
        );
        */

    }

}

export const repositoryApi =
    new RepositoryApi();
