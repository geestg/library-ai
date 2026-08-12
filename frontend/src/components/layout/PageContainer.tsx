import { ReactNode } from "react";
import { colors, typography } from "../../design";

interface Props {
    title: string;
    description?: string;
    action?: ReactNode;
    children: ReactNode;
}

export default function PageContainer({
    title,
    description,
    action,
    children,
}: Props) {
    return (
        <div
            style={{
                width: "100%",
                maxWidth: 1280,
                margin: "0 auto",
            }}
        >
            <header
                style={{
                    display: "flex",
                    alignItems: "flex-start",
                    justifyContent: "space-between",
                    gap: 24,
                    marginBottom: 24,
                }}
            >
                <div>
                    <h1
                        style={{
                            ...typography.h1,
                            margin: 0,
                            color: colors.text,
                        }}
                    >
                        {title}
                    </h1>

                    {description && (
                        <p
                            style={{
                                ...typography.body,
                                margin: "8px 0 0",
                                maxWidth: 760,
                                color: colors.textSecondary,
                            }}
                        >
                            {description}
                        </p>
                    )}
                </div>

                {action && (
                    <div
                        style={{
                            flexShrink: 0,
                        }}
                    >
                        {action}
                    </div>
                )}
            </header>

            {children}
        </div>
    );
}
