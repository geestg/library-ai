import { jsx as _jsx } from "react/jsx-runtime";
import { colors } from "../../design";
export default function Button(props) {
    return (_jsx("button", { ...props, style: {
            height: 36,
            padding: "0 14px",
            borderRadius: 8,
            border: "none",
            cursor: "pointer",
            background: colors.primary,
            color: "#fff",
            fontWeight: 600,
            ...props.style,
        } }));
}
