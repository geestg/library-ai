import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { colors, typography } from "../../design";
export default function PageContainer({ title, description, action, children, }) {
    return (_jsxs("div", { style: {
            width: "100%",
            maxWidth: 1280,
            margin: "0 auto",
        }, children: [_jsxs("header", { style: {
                    display: "flex",
                    alignItems: "flex-start",
                    justifyContent: "space-between",
                    gap: 24,
                    marginBottom: 24,
                }, children: [_jsxs("div", { children: [_jsx("h1", { style: {
                                    ...typography.h1,
                                    margin: 0,
                                    color: colors.text,
                                }, children: title }), description && (_jsx("p", { style: {
                                    ...typography.body,
                                    margin: "8px 0 0",
                                    maxWidth: 760,
                                    color: colors.textSecondary,
                                }, children: description }))] }), action && (_jsx("div", { style: {
                            flexShrink: 0,
                        }, children: action }))] }), children] }));
}
