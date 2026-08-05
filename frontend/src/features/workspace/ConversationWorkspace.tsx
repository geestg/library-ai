import { colors, typography } from "../../design";
import { Card } from "../../components/ui";
import ResearchInputDock from "./ResearchInputDock";
import WorkspaceEmptyState from "./WorkspaceEmptyState";
import CitationPanel from "./CitationPanel";
import Conversation from "../conversation/Conversation";

const workspaceStyle: React.CSSProperties = {
    flex: 1,
    display: "flex",
    background: colors.background,
    overflow: "hidden",
};

const conversationStyle: React.CSSProperties = {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    padding: 32,
    gap: 24,
    overflowY: "auto",
};

export default function ConversationWorkspace() {

    return (

        <section style={workspaceStyle}>

            <div style={conversationStyle}>

                <Card>

                    <div
                        style={{
                            ...typography.h2,
                            marginBottom: 8,
                        }}
                    >
                        Research Workspace
                    </div>

                    <div
                        style={{
                            ...typography.body,
                            color: colors.textSecondary,
                            lineHeight: 1.7,
                        }}
                    >
                        Ask academic questions, compare papers, discover
                        research gaps, generate thesis ideas, and explore
                        your knowledge base with evidence-backed answers.
                    </div>

                </Card>

                <div
                    style={{
                        flex: 1,
                        border: `1px dashed ${colors.border}`,
                        borderRadius: 12,
                        background: colors.surface,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        color: colors.textSecondary,
                    }}
                >
                    Conversation Stream
                </div>

                <ResearchInputDock />

            </div>

            <CitationPanel />

        </section>

    );

}
