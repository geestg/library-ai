import { useEffect, useState } from "react";
import { RefreshCw, FileText, CheckCircle2, AlertCircle } from "lucide-react";

import { repositoryExplorer } from "../../api/repository";
import WorkspaceShell from "../../components/layout/WorkspaceShell";
import PageContainer from "../../components/layout/PageContainer";
import PageSection from "../../components/layout/PageSection";
import { colors, spacing, typography, radius } from "../../design";

type RepositoryItem = {
    id: string;
    title: string;
    status: string;
    local_path?: string | null;
};

type RepositoryResponse = {
    total: number;
    pdf_available: number;
    pdf_missing: number;
    items: RepositoryItem[];
};

export default function RepositoryPage() {
    const [data, setData] = useState<RepositoryResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    async function loadRepository() {
        setLoading(true);
        setError("");

        try {
            const response = await repositoryExplorer();
            setData(response.data);
        } catch {
            setData(null);
            setError("Unable to load repository.");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadRepository();
    }, []);

    return (
        <WorkspaceShell>
            <PageContainer
                title="Repository"
                description="Manage and inspect the academic documents available to DELBot."
                action={
                    <button
                        type="button"
                        onClick={loadRepository}
                        disabled={loading}
                        style={{
                            height: 36,
                            padding: "0 14px",
                            display: "inline-flex",
                            alignItems: "center",
                            gap: 8,
                            border: `1px solid ${colors.border}`,
                            borderRadius: radius.sm,
                            background: colors.surface,
                            color: colors.text,
                            fontWeight: 600,
                            cursor: loading ? "default" : "pointer",
                        }}
                    >
                        <RefreshCw size={15} />
                        {loading ? "Loading..." : "Refresh"}
                    </button>
                }
            >
                {error && (
                    <PageSection
                        style={{
                            padding: spacing.lg,
                            marginBottom: spacing.xl,
                        }}
                    >
                        <div
                            style={{
                                display: "flex",
                                alignItems: "center",
                                gap: 10,
                                color: colors.danger,
                                ...typography.bodyMedium,
                            }}
                        >
                            <AlertCircle size={17} />
                            {error}
                        </div>
                    </PageSection>
                )}

                <div
                    style={{
                        display: "grid",
                        gridTemplateColumns:
                            "repeat(3, minmax(0, 1fr))",
                        gap: spacing.md,
                        marginBottom: spacing.xl,
                    }}
                >
                    <PageSection style={{ padding: spacing.lg }}>
                        <div style={typography.caption}>
                            Repository Documents
                        </div>
                        <div
                            style={{
                                ...typography.h2,
                                marginTop: 6,
                            }}
                        >
                            {data?.total ?? 0}
                        </div>
                    </PageSection>

                    <PageSection style={{ padding: spacing.lg }}>
                        <div style={typography.caption}>
                            PDF Available
                        </div>
                        <div
                            style={{
                                ...typography.h2,
                                marginTop: 6,
                                color: colors.success,
                            }}
                        >
                            {data?.pdf_available ?? 0}
                        </div>
                    </PageSection>

                    <PageSection style={{ padding: spacing.lg }}>
                        <div style={typography.caption}>
                            Metadata Only
                        </div>
                        <div
                            style={{
                                ...typography.h2,
                                marginTop: 6,
                                color: colors.warning,
                            }}
                        >
                            {data?.pdf_missing ?? 0}
                        </div>
                    </PageSection>
                </div>

                <PageSection>
                    <div
                        style={{
                            padding: `${spacing.lg}px ${spacing.xl}px`,
                            borderBottom:
                                `1px solid ${colors.border}`,
                            display: "flex",
                            alignItems: "center",
                            gap: 10,
                        }}
                    >
                        <FileText size={18} />
                        <div>
                            <div style={typography.h4}>
                                Repository Contents
                            </div>
                            <div
                                style={{
                                    ...typography.caption,
                                    color: colors.textSecondary,
                                }}
                            >
                                Documents currently visible to DELBot.
                            </div>
                        </div>
                    </div>

                    {loading && !data ? (
                        <div
                            style={{
                                padding: 32,
                                color: colors.textSecondary,
                            }}
                        >
                            Loading repository...
                        </div>
                    ) : data?.items?.length ? (
                        <div>
                            {data.items.map((item) => {
                                const available =
                                    item.status === "pdf_available";

                                return (
                                    <div
                                        key={item.id}
                                        style={{
                                            display: "grid",
                                            gridTemplateColumns:
                                                "minmax(0, 1fr) auto",
                                            gap: spacing.lg,
                                            alignItems: "center",
                                            padding:
                                                `${spacing.md}px ${spacing.xl}px`,
                                            borderBottom:
                                                `1px solid ${colors.borderLight}`,
                                        }}
                                    >
                                        <div
                                            style={{
                                                minWidth: 0,
                                            }}
                                        >
                                            <div
                                                style={{
                                                    ...typography.bodyMedium,
                                                    color: colors.text,
                                                    overflow: "hidden",
                                                    textOverflow:
                                                        "ellipsis",
                                                    whiteSpace: "nowrap",
                                                }}
                                                title={item.title}
                                            >
                                                {item.title}
                                            </div>

                                            <div
                                                style={{
                                                    ...typography.caption,
                                                    color: colors.textMuted,
                                                    marginTop: 3,
                                                }}
                                            >
                                                {item.id}
                                            </div>
                                        </div>

                                        <div
                                            style={{
                                                display: "inline-flex",
                                                alignItems: "center",
                                                gap: 6,
                                                padding: "5px 9px",
                                                borderRadius:
                                                    radius.sm,
                                                border:
                                                    `1px solid ${colors.border}`,
                                                color: available
                                                    ? colors.success
                                                    : colors.textSecondary,
                                                background:
                                                    colors.surfaceSecondary,
                                                ...typography.caption,
                                                whiteSpace: "nowrap",
                                            }}
                                        >
                                            <CheckCircle2
                                                size={14}
                                            />
                                            {available
                                                ? "PDF available"
                                                : "Metadata only"}
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    ) : (
                        <div
                            style={{
                                padding: 32,
                                color: colors.textSecondary,
                            }}
                        >
                            No repository documents found.
                        </div>
                    )}
                </PageSection>
            </PageContainer>
        </WorkspaceShell>
    );
}
