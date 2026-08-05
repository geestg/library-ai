import { jsx as _jsx } from "react/jsx-runtime";
import { colors } from "../../design";
export default function Divider() {
    return (_jsx("div", { style: {
            width: "100%",
            height: 1,
            background: colors.border,
        } }));
}
