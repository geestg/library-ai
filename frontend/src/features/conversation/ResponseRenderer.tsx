import { Card } from "../../components/ui";
import { typography } from "../../design";
import MarkdownRenderer from "../../components/markdown/MarkdownRenderer";

export interface ResponseRendererProps {
    content?: string;
}

export default function ResponseRenderer({
    content = "",
}: ResponseRendererProps) {

    return (

        <Card
            style={{
                marginTop:24,
            }}
        >

            <div style={typography.h4}>
                DELBot Response
            </div>

            <div style={{height:16}} />

            <MarkdownRenderer
                content={content}
            />

        </Card>

    );
}
