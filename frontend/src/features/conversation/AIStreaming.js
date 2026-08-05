import { jsx as _jsx } from "react/jsx-runtime";
import { Card } from "../../components/ui";
import { colors, typography } from "../../design";
export default function AIStreaming({ streaming = false, }) {
    if (!streaming)
        return null;
    return (_jsx(Card, { style: {
            marginTop: 16,
            padding: 18,
            borderColor: colors.primarySoft,
            background: colors.surface,
        }, children: _jsx("div", { style: typography.bodyMedium, children: "DELBot is generating an academic response..." }) }));
}
