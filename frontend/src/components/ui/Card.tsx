import { ReactNode } from "react";
import { colors } from "../../design";

interface Props {
    children: ReactNode;
    style?: React.CSSProperties;
}

export default function Card({
    children,
    style,
}: Props) {

    return (
        <div
            style={{
                background: colors.surface,
                border: `1px solid ${colors.border}`,
                borderRadius: 12,
                boxShadow:
                    "0 1px 2px rgba(15,23,42,.04)",
                ...style,
            }}
        >
            {children}
        </div>
    );
}
