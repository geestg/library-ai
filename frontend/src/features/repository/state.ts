import { RepositoryDocument } from "../../types/repository";

export interface RepositoryState {

    loading: boolean;

    documents: RepositoryDocument[];

    selected?: RepositoryDocument;

}

export const initialRepositoryState: RepositoryState = {

    loading: false,

    documents: [],

    selected: undefined,

};
