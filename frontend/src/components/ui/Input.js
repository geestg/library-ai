import { jsx as _jsx } from "react/jsx-runtime";
import { colors } from "../../design";
export default function Input(props) {
    return (_jsx("input", { ...props, style: {
            width: "100%",
            height: 40,
            padding: "0 14px",
            borderRadius: 8,
            border: `1px solid ${colors.border}`,
            outline: "none",
            background: colors.surface,
            ...props.style,
        } }));
}
