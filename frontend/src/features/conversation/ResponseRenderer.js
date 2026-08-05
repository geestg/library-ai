import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card } from "../../components/ui";
import { typography } from "../../design";
import MarkdownRenderer from "../../components/markdown/MarkdownRenderer";
export default function ResponseRenderer({ content = "", }) {
    return (_jsxs(Card, { style: {
            marginTop: 24,
        }, children: [_jsx("div", { style: typography.h4, children: "DELBot Response" }), _jsx("div", { style: { height: 16 } }), _jsx(MarkdownRenderer, { content: content })] }));
}
