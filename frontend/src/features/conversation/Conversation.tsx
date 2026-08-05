import { Card } from "../../components/ui";
import { typography, colors } from "../../design";
import AIStreaming from "./AIStreaming";
import ResponseRenderer from "./ResponseRenderer";

export default function Conversation() {

    return (

        <Card
            style={{
                flex: 1,
                display: "flex",
                flexDirection: "column",
                gap: 24,
                padding: 32,
                background: colors.surface,
            }}
        >

            <div>

                <div style={typography.h3}>
                    Conversation
                </div>

                <div
                    style={{
                        ...typography.body,
                        color: colors.textSecondary,
                        marginTop: 8,
                    }}
                >
                    Ask questions, compare papers, discover research gaps,
                    and generate thesis ideas from your repository.
                </div>

            </div>

            <div
                style={{
                    flex: 1,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    border: `1px dashed ${colors.border}`,
                    borderRadius: 12,
                    background: colors.surfaceSecondary,
                    minHeight: 320,
                }}
            >

                <div
                    style={{
                        ...typography.body,
                        color: colors.textSecondary,
                    }}
                >
                    Conversation Stream
                </div>

            </div>

            <ResponseRenderer />

            <AIStreaming />

        </Card>

    );

}
