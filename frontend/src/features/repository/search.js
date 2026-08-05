export class RepositorySearcher {
    async search(request) {
        return {
            query: request.query,
            results: [],
        };
    }
}
export const repositorySearcher = new RepositorySearcher();
