import { useEffect, useMemo, useState } from "react";
import {
    Search,
    FolderOpen,
    FileText,
    CheckCircle2,
    AlertCircle,
} from "lucide-react";
import { repositoryExplorer } from "../../api/repository";

type RepositoryItem = {
    id?: string;
    title?: string;
    filename?: string;
    document_name?: string;
    document_id?: string;
    status?: string;
    local_path?: string | null;
};

type RepositoryResponse = {
    total: number;
    pdf_available: number;
    pdf_missing: number;
    items: RepositoryItem[];
};

export default function RepositoryPage() {

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [keyword, setKeyword] = useState("");

    const [repo, setRepo] = useState<RepositoryResponse>({
        total: 0,
        pdf_available: 0,
        pdf_missing: 0,
        items: [],
    });

    useEffect(() => {

        repositoryExplorer()
            .then((res) => {

                setRepo({
                    total: res.data.total ?? 0,
                    pdf_available: res.data.pdf_available ?? 0,
                    pdf_missing: res.data.pdf_missing ?? 0,
                    items: res.data.items ?? [],
                });

            })
            .catch((err) => {
                setError(err?.message ?? "Failed to load repository.");
            })
            .finally(() => {
                setLoading(false);
            });

    }, []);

    const filtered = useMemo(() => {

        const q = keyword.trim().toLowerCase();

        if (!q) {
            return repo.items;
        }

        return repo.items.filter((item) => {

            const title =
                item.title ??
                item.filename ??
                item.document_name ??
                item.document_id ??
                "";

            return title.toLowerCase().includes(q);

        });

    }, [repo.items, keyword]);

    const statCard: React.CSSProperties = {
        background: "#ffffff",
        border: "1px solid #e5e7eb",
        borderRadius: 12,
        padding: 20,
        flex: 1,
        minWidth: 180,
        boxShadow: "0 1px 4px rgba(0,0,0,.05)",
    };

    const tableHeader: React.CSSProperties = {
        padding: 14,
        textAlign: "left",
        background: "#f8fafc",
        borderBottom: "1px solid #e5e7eb",
        fontWeight: 600,
    };

    const tableCell: React.CSSProperties = {
        padding: 14,
        borderBottom: "1px solid #f1f5f9",
    };

    if (loading) {
        return <h3>Loading repository...</h3>;
    }

    if (error) {
        return <h3>{error}</h3>;
    }

    return (

        <div>

            <div
                style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginBottom: 28,
                    flexWrap: "wrap",
                    gap: 16,
                }}
            >

                <div>

                    <h1 style={{ margin: 0 }}>
                        Repository Explorer
                    </h1>

                    <p
                        style={{
                            marginTop: 8,
                            color: "#6b7280",
                        }}
                    >
                        Browse repository documents.
                    </p>

                </div>

                <div
                    style={{
                        display: "flex",
                        alignItems: "center",
                        gap: 8,
                        background: "#eff6ff",
                        color: "#1d4ed8",
                        padding: "10px 16px",
                        borderRadius: 999,
                        fontWeight: 600,
                    }}
                >
                    <FolderOpen size={18} />
                    {repo.total} Documents
                </div>

            </div>

            <div
                style={{
                    display: "flex",
                    gap: 18,
                    flexWrap: "wrap",
                    marginBottom: 28,
                }}
            >

                <div style={statCard}>
                    <div>Total Repository</div>
                    <h2>{repo.total}</h2>
                </div>

                <div style={statCard}>
                    <div>PDF Available</div>
                    <h2>{repo.pdf_available}</h2>
                </div>

                <div style={statCard}>
                    <div>PDF Missing</div>
                    <h2>{repo.pdf_missing}</h2>
                </div>

                <div style={statCard}>
                    <div>Showing</div>
                    <h2>{filtered.length}</h2>
                </div>

            </div>

            <div
                style={{
                    position: "relative",
                    marginBottom: 24,
                }}
            >

                <Search
                    size={18}
                    style={{
                        position: "absolute",
                        left: 14,
                        top: 14,
                        color: "#9ca3af",
                    }}
                />

                <input
                    type="text"
                    placeholder="Search document..."
                    value={keyword}
                    onChange={(e) => setKeyword(e.target.value)}
                    style={{
                        width: "100%",
                        padding: "12px 16px 12px 42px",
                        border: "1px solid #d1d5db",
                        borderRadius: 10,
                        boxSizing: "border-box",
                        fontSize: 15,
                    }}
                />

            </div>

            <div
                style={{
                    background: "#ffffff",
                    border: "1px solid #e5e7eb",
                    borderRadius: 12,
                    overflow: "hidden",
                    boxShadow: "0 1px 4px rgba(0,0,0,.05)",
                }}
            >

                <table
                    style={{
                        width: "100%",
                        borderCollapse: "collapse",
                    }}
                >

                    <thead>

                        <tr>

                            <th style={tableHeader}>
                                #
                            </th>

                            <th style={tableHeader}>
                                Document
                            </th>

                            <th style={tableHeader}>
                                Status
                            </th>

                        </tr>

                    </thead>

                    <tbody>

                        {filtered.length === 0 && (

                            <tr>

                                <td
                                    colSpan={3}
                                    style={{
                                        padding: 40,
                                        textAlign: "center",
                                        color: "#6b7280",
                                    }}
                                >
                                    No document found.
                                </td>

                            </tr>

                        )}

                        {filtered.map((item, index) => {

                            const title =
                                item.title ??
                                item.filename ??
                                item.document_name ??
                                item.document_id ??
                                "Untitled";

                            const ok =
                                item.status === "pdf_available";

                            return (

                                <tr
                                    key={
                                        item.id ??
                                        item.document_id ??
                                        index
                                    }
                                >

                                    <td style={tableCell}>
                                        {index + 1}
                                    </td>

                                    <td style={tableCell}>

                                        <div
                                            style={{
                                                display: "flex",
                                                alignItems: "center",
                                                gap: 10,
                                            }}
                                        >

                                            <FileText
                                                size={18}
                                                color="#2563eb"
                                            />

                                            {title}

                                        </div>

                                    </td>

                                    <td style={tableCell}>

                                        <div
                                            style={{
                                                display: "inline-flex",
                                                alignItems: "center",
                                                gap: 6,
                                                padding: "5px 10px",
                                                borderRadius: 999,
                                                background: ok
                                                    ? "#dcfce7"
                                                    : "#fef3c7",
                                                color: ok
                                                    ? "#166534"
                                                    : "#92400e",
                                                fontSize: 13,
                                                fontWeight: 600,
                                            }}
                                        >

                                            {ok ? (
                                                <CheckCircle2 size={15} />
                                            ) : (
                                                <AlertCircle size={15} />
                                            )}

                                            {item.status ?? "-"}

                                        </div>

                                    </td>

                                </tr>

                            );

                        })}

                    </tbody>

                </table>

            </div>

        </div>

    );

}
