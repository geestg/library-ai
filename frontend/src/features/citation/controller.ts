import type { RepositoryDocument } from "../../types/repository";

export interface CitationSelection {

    document: RepositoryDocument;

    page?: number;

    chunkId?: string;

}

export type CitationListener =
    (selection: CitationSelection) => void;

export class CitationController {

    select(

        selection: CitationSelection,

        listener?: CitationListener,

    ): CitationSelection {

        listener?.(selection);

        return selection;

    }

}

export const citationController =
    new CitationController();
