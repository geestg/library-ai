import { colors, typography } from "../../design";
import { Button, Input } from "../../components/ui";

const containerStyle: React.CSSProperties = {
    padding: 24,
    borderTop: `1px solid ${colors.border}`,
    background: colors.surface,
};

const wrapperStyle: React.CSSProperties = {
    maxWidth: 920,
    margin: "0 auto",
    display: "flex",
    flexDirection: "column",
    gap: 14,
};

const rowStyle: React.CSSProperties = {
    display: "flex",
    gap: 12,
    alignItems: "center",
};

export default function ResearchInputDock() {

    return (

        <footer style={containerStyle}>

            <div style={wrapperStyle}>

                <Input
                    placeholder="Ask a research question, compare papers, summarize literature..."
                />

                <div
                    style={{
                        ...rowStyle,
                        justifyContent: "space-between",
                    }}
                >

                    <div
                        style={{
                            ...typography.caption,
                            color: colors.textSecondary,
                        }}
                    >
                        Answers are generated from indexed repository documents with citations.
                    </div>

                    <Button>
                        Ask DELBot
                    </Button>

                </div>

            </div>

        </footer>

    );

}
