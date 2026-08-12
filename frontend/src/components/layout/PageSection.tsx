import { ReactNode } from "react";
import { colors, radius, shadow } from "../../design";

interface Props {
    children: ReactNode;
    style?: React.CSSProperties;
}

export default function PageSection({
    children,
    style,
}: Props) {
    return (
        <section
            style={{
                background: colors.surface,
                border: `1px solid ${colors.border}`,
                borderRadius: radius.md,
                boxShadow: shadow.sm,
                ...style,
            }}
        >
            {children}
        </section>
    );
}
