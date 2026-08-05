import { apiClient } from "./client";
export class RepositoryApi {
    async upload(request) {
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
export const repositoryApi = new RepositoryApi();
