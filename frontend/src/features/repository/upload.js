import { repositoryBackend, } from "./backend";
export class RepositoryUploadFlow {
    async upload(upload) {
        return repositoryBackend.upload({
            files: upload.files,
        });
    }
}
export const repositoryUploadFlow = new RepositoryUploadFlow();
