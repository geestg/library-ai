export class CitationController {
    select(selection, listener) {
        listener?.(selection);
        return selection;
    }
}
export const citationController = new CitationController();
