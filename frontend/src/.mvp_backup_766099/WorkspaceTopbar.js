import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { colors, typography } from "../../design";
const topbarStyle = {
    height: 60,
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "0 24px",
    borderBottom: `1px solid ${colors.border}`,
    background: colors.surface,
};
const leftStyle = {
    display: "flex",
    flexDirection: "column",
    gap: 2,
};
export default function WorkspaceTopbar() {
    return (_jsx("header", { style: topbarStyle, children: _jsxs("div", { style: leftStyle, children: [_jsx("span", { style: {
                        ...typography.h3,
                        color: colors.text,
                    }, children: "DELBot" }), _jsx("span", { style: {
                        ...typography.caption,
                        color: colors.textSecondary,
                    } })] }) }));
}
