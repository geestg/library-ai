import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from "react";
import { RefreshCw, FileText, CheckCircle2, AlertCircle } from "lucide-react";
import { repositoryExplorer, repositoryScan } from "../../api/repository";
import { indexRepository } from "../../api/document";
import WorkspaceShell from "../../components/layout/WorkspaceShell";
import PageContainer from "../../components/layout/PageContainer";
import PageSection from "../../components/layout/PageSection";
import { colors, spacing, typography, radius } from "../../design";
export default function RepositoryPage() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [scanning, setScanning] = useState(false);
    const [indexing, setIndexing] = useState(false);
    const [error, setError] = useState("");
    async function loadRepository() {
        setLoading(true);
        setError("");
        try {
            const response = await repositoryExplorer();
            setData(response.data);
        }
        catch {
            setData(null);
            setError("Unable to load repository.");
        }
        finally {
            setLoading(false);
        }
    }
    async function handleScan() {
        setScanning(true);
        setError("");
        try {
            await repositoryScan(".");
            await loadRepository();
        }
        catch {
            setError("Unable to scan repository.");
        }
        finally {
            setScanning(false);
        }
    }
    async function handleIndex() {
        setIndexing(true);
        setError("");
        try {
            await indexRepository(25);
            await loadRepository();
        }
        catch {
            setError("Unable to index repository.");
        }
        finally {
            setIndexing(false);
        }
    }
    useEffect(() => {
        loadRepository();
    }, []);
    return (_jsx(WorkspaceShell, { children: _jsxs(PageContainer, { title: "Repository", description: "Manage and inspect the academic documents available to DELBot.", action: _jsxs("div", { style: {
                    display: "flex",
                    alignItems: "center",
                    gap: 8,
                    flexWrap: "wrap",
                }, children: [_jsxs("button", { type: "button", onClick: handleScan, disabled: scanning, style: {
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
                            cursor: scanning ? "default" : "pointer",
                        }, children: [_jsx(RefreshCw, { size: 15 }), scanning ? "Scanning..." : "Scan Repository"] }), _jsxs("button", { type: "button", onClick: handleIndex, disabled: indexing, style: {
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
                            cursor: indexing ? "default" : "pointer",
                        }, children: [_jsx(FileText, { size: 15 }), indexing ? "Indexing..." : "Index Documents"] }), _jsxs("button", { type: "button", onClick: loadRepository, disabled: loading, style: {
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
                        }, children: [_jsx(RefreshCw, { size: 15 }), loading ? "Loading..." : "Refresh"] })] }), children: [error && (_jsx(PageSection, { style: {
                        padding: spacing.lg,
                        marginBottom: spacing.xl,
                    }, children: _jsxs("div", { style: {
                            display: "flex",
                            alignItems: "center",
                            gap: 10,
                            color: colors.danger,
                            ...typography.bodyMedium,
                        }, children: [_jsx(AlertCircle, { size: 17 }), error] }) })), _jsxs("div", { style: {
                        display: "grid",
                        gridTemplateColumns: "repeat(3, minmax(0, 1fr))",
                        gap: spacing.md,
                        marginBottom: spacing.xl,
                    }, children: [_jsxs(PageSection, { style: { padding: spacing.lg }, children: [_jsx("div", { style: typography.caption, children: "Repository Documents" }), _jsx("div", { style: {
                                        ...typography.h2,
                                        marginTop: 6,
                                    }, children: data?.total ?? 0 })] }), _jsxs(PageSection, { style: { padding: spacing.lg }, children: [_jsx("div", { style: typography.caption, children: "PDF Available" }), _jsx("div", { style: {
                                        ...typography.h2,
                                        marginTop: 6,
                                        color: colors.success,
                                    }, children: data?.pdf_available ?? 0 })] }), _jsxs(PageSection, { style: { padding: spacing.lg }, children: [_jsx("div", { style: typography.caption, children: "Metadata Only" }), _jsx("div", { style: {
                                        ...typography.h2,
                                        marginTop: 6,
                                        color: colors.warning,
                                    }, children: data?.pdf_missing ?? 0 })] })] }), _jsxs(PageSection, { children: [_jsxs("div", { style: {
                                padding: `${spacing.lg}px ${spacing.xl}px`,
                                borderBottom: `1px solid ${colors.border}`,
                                display: "flex",
                                alignItems: "center",
                                gap: 10,
                            }, children: [_jsx(FileText, { size: 18 }), _jsxs("div", { children: [_jsx("div", { style: typography.h4, children: "Repository Contents" }), _jsx("div", { style: {
                                                ...typography.caption,
                                                color: colors.textSecondary,
                                            }, children: "Documents currently visible to DELBot." })] })] }), loading && !data ? (_jsx("div", { style: {
                                padding: 32,
                                color: colors.textSecondary,
                            }, children: "Loading repository..." })) : data?.items?.length ? (_jsx("div", { children: data.items.map((item) => {
                                const available = item.status === "pdf_available";
                                return (_jsxs("div", { style: {
                                        display: "grid",
                                        gridTemplateColumns: "minmax(0, 1fr) auto",
                                        gap: spacing.lg,
                                        alignItems: "center",
                                        padding: `${spacing.md}px ${spacing.xl}px`,
                                        borderBottom: `1px solid ${colors.borderLight}`,
                                    }, children: [_jsxs("div", { style: {
                                                minWidth: 0,
                                            }, children: [_jsx("div", { style: {
                                                        ...typography.bodyMedium,
                                                        color: colors.text,
                                                        overflow: "hidden",
                                                        textOverflow: "ellipsis",
                                                        whiteSpace: "nowrap",
                                                    }, title: item.title, children: item.title }), _jsx("div", { style: {
                                                        ...typography.caption,
                                                        color: colors.textMuted,
                                                        marginTop: 3,
                                                    }, children: item.id })] }), _jsxs("div", { style: {
                                                display: "inline-flex",
                                                alignItems: "center",
                                                gap: 6,
                                                padding: "5px 9px",
                                                borderRadius: radius.sm,
                                                border: `1px solid ${colors.border}`,
                                                color: available
                                                    ? colors.success
                                                    : colors.textSecondary,
                                                background: colors.surfaceSecondary,
                                                ...typography.caption,
                                                whiteSpace: "nowrap",
                                            }, children: [_jsx(CheckCircle2, { size: 14 }), available
                                                    ? "PDF available"
                                                    : "Metadata only"] })] }, item.id));
                            }) })) : (_jsx("div", { style: {
                                padding: 32,
                                color: colors.textSecondary,
                            }, children: "No repository documents found." }))] })] }) }));
}
