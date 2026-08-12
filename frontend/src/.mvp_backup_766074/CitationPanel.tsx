import { colors, typography } from "../../design";
import Citation from "../../components/citation/Citation";
import PDFEvidenceViewer from "../../components/pdf/PDFEvidenceViewer";

const panelStyle: React.CSSProperties = {
    width: 340,
    display: "flex",
    flexDirection: "column",
    background: colors.surface,
    borderLeft: `1px solid ${colors.border}`,
};

const bodyStyle: React.CSSProperties = {
    padding: 20,
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    gap: 16,
};

export default function CitationPanel() {

    
return (

<aside style={panelStyle}>

    <><Citation /><PDFEvidenceViewer /></>

</aside>

);


}
