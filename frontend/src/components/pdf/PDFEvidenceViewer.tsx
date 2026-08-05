import { Card } from "../../components/ui";
import { colors, typography } from "../../design";

export interface PDFEvidenceViewerProps {
    title?: string;
    page?: number;
}

export default function PDFEvidenceViewer({
    title = "No document selected",
    page,
}: PDFEvidenceViewerProps) {

    return (

        <Card
            style={{
                marginTop:24,
                display:"flex",
                flexDirection:"column",
                gap:16,
                minHeight:320,
            }}
        >

            <div style={typography.h4}>
                PDF Preview
            </div>

            <div
                style={{
                    ...typography.caption,
                    color:colors.textSecondary,
                }}
            >
                {title}
            </div>

            <div
                style={{
                    flex:1,
                    minHeight:220,
                    border:`1px dashed ${colors.border}`,
                    borderRadius:10,
                    background:colors.surfaceSecondary,
                    display:"flex",
                    alignItems:"center",
                    justifyContent:"center",
                    color:colors.textMuted,
                    textAlign:"center",
                    padding:32,
                }}
            >
                PDF Preview Area

                {page
                    ? ` (Page ${page})`
                    : ""}
            </div>

        </Card>

    );

}
