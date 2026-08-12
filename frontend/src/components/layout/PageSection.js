import { jsx as _jsx } from "react/jsx-runtime";
import { colors, radius, shadow } from "../../design";
export default function PageSection({ children, style, }) {
    return (_jsx("section", { style: {
            background: colors.surface,
            border: `1px solid ${colors.border}`,
            borderRadius: radius.md,
            boxShadow: shadow.sm,
            ...style,
        }, children: children }));
}
