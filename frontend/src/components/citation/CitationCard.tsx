import { Card, Divider } from "../../components/ui";
import { typography, colors } from "../../design";

export interface CitationCardProps {
    title?: string;
    author?: string;
    year?: string;
    source?: "fulltext" | "metadata";
    page?: number;
}

export default function CitationCard({
    title = "Waiting for citation...",
    author,
    year,
    source = "fulltext",
    page,
}: CitationCardProps) {

    return (

        <Card
            style={{
                display: "flex",
                flexDirection: "column",
                gap: 10,
            }}
        >

            <div style={typography.h4}>
                {title}
            </div>

            <Divider />

            <div
                style={{
                    ...typography.caption,
                    color: colors.textSecondary,
                    display: "flex",
                    flexDirection: "column",
                    gap: 4,
                }}
            >

                {author && <div>Author : {author}</div>}
                {year && <div>Year : {year}</div>}

                <div>
                    Source :
                    {" "}
                    {source === "fulltext"
                        ? "Fulltext PDF"
                        : "Metadata Abstract"}
                </div>

                {page && (
                    <div>
                        Page : {page}
                    </div>
                )}

            </div>

        </Card>

    );
}
