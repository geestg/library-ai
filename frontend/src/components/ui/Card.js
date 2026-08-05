import { jsx as _jsx } from "react/jsx-runtime";
import { colors } from "../../design";
export default function Card({ children, style, }) {
    return (_jsx("div", { style: {
            background: colors.surface,
            border: `1px solid ${colors.border}`,
            borderRadius: 12,
            boxShadow: "0 1px 2px rgba(15,23,42,.04)",
            ...style,
        }, children: children }));
}
