import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card } from "../../components/ui";
import { typography, colors } from "../../design";
import AIStreaming from "./AIStreaming";
import ResponseRenderer from "./ResponseRenderer";
export default function Conversation() {
    return (_jsxs(Card, { style: {
            flex: 1,
            display: "flex",
            flexDirection: "column",
            gap: 24,
            padding: 32,
            background: colors.surface,
        }, children: [_jsxs("div", { children: [_jsx("div", { style: typography.h3, children: "Conversation" }), _jsx("div", { style: {
                            ...typography.body,
                            color: colors.textSecondary,
                            marginTop: 8,
                        }, children: "Ask questions, compare papers, discover research gaps, and generate thesis ideas from your repository." })] }), _jsx("div", { style: {
                    flex: 1,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    border: `1px dashed ${colors.border}`,
                    borderRadius: 12,
                    background: colors.surfaceSecondary,
                    minHeight: 320,
                }, children: _jsx("div", { style: {
                        ...typography.body,
                        color: colors.textSecondary,
                    }, children: "Conversation Stream" }) }), _jsx(ResponseRenderer, {}), _jsx(AIStreaming, {})] }));
}
