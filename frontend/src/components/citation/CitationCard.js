import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card, Divider } from "../../components/ui";
import { typography, colors } from "../../design";
export default function CitationCard({ title = "Waiting for citation...", author, year, source = "fulltext", page, }) {
    return (_jsxs(Card, { style: {
            display: "flex",
            flexDirection: "column",
            gap: 10,
        }, children: [_jsx("div", { style: typography.h4, children: title }), _jsx(Divider, {}), _jsxs("div", { style: {
                    ...typography.caption,
                    color: colors.textSecondary,
                    display: "flex",
                    flexDirection: "column",
                    gap: 4,
                }, children: [author && _jsxs("div", { children: ["Author : ", author] }), year && _jsxs("div", { children: ["Year : ", year] }), _jsxs("div", { children: ["Source :", " ", source === "fulltext"
                                ? "Fulltext PDF"
                                : "Metadata Abstract"] }), page && (_jsxs("div", { children: ["Page : ", page] }))] })] }));
}
