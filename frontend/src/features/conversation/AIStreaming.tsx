import { Card } from "../../components/ui";
import { colors, typography } from "../../design";

export interface AIStreamingProps {
    streaming?: boolean;
}

export default function AIStreaming({
    streaming = false,
}: AIStreamingProps) {

    if (!streaming) return null;

    return (
        <Card
            style={{
                marginTop: 16,
                padding: 18,
                borderColor: colors.primarySoft,
                background: colors.surface,
            }}
        >
            <div style={typography.bodyMedium}>
                DELBot is generating an academic response...
            </div>
        </Card>
    );
}
