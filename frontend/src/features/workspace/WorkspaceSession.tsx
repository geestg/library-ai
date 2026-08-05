import { Card } from "../../components/ui";
import { typography, colors } from "../../design";

export default function WorkspaceSession() {

    return (

        <Card
            style={{
                marginTop:16,
                background:colors.surfaceSecondary,
            }}
        >

            <div style={typography.label}>
                Current Workspace
            </div>

            <div
                style={{
                    ...typography.bodyMedium,
                    marginTop:8,
                    color:colors.text,
                }}
            >
                Untitled Research
            </div>

            <div
                style={{
                    ...typography.caption,
                    marginTop:6,
                    color:colors.textSecondary,
                }}
            >
                No conversation history yet.
            </div>

        </Card>

    );

}
