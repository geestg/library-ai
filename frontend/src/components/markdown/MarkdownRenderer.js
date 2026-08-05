import { jsx as _jsx } from "react/jsx-runtime";
import { colors, typography } from "../../design";
const containerStyle = {
    ...typography.body,
    color: colors.text,
    lineHeight: 1.8,
    whiteSpace: "pre-wrap",
    wordBreak: "break-word",
};
export default function MarkdownRenderer({ content = "", }) {
    return (_jsx("div", { style: containerStyle, children: content.length > 0
            ? content
            : "AI response will be rendered here." }));
}
