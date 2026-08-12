import WorkspaceShell from "../../components/layout/WorkspaceShell";
import { useEffect, useState } from "react";
import { repositoryExplorer } from "../../api/repository";

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

    useEffect(() => {
        repositoryExplorer()
            .then((response) => {
                setData(response.data);
                setError("");
            })
            .catch(() => {
                setError("Unable to load repository.");
            })
            .finally(() => {
                setLoading(false);
            });
    }, []);

    return (
        <WorkspaceShell>
        <main
            style={{
                padding: 32,
                maxWidth: 1200,
                margin: "0 auto",
                fontFamily: "Inter, system-ui, sans-serif",
            }}
        >
            <h1 style={{ marginBottom: 8 }}>
                Repository
            </h1>

            <p style={{ color: "#64748b", marginBottom: 24 }}>
                Browse documents available in the academic repository.
            </p>

            {loading && (
                <p>Loading repository...</p>
            )}

            {error && (
                <p style={{ color: "#b91c1c" }}>
                    {error}
                </p>
            )}

            {data && (
                <>
                    <div
                        style={{
                            display: "grid",
                            gridTemplateColumns:
                                "repeat(3, minmax(0, 1fr))",
                            gap: 12,
                            marginBottom: 24,
                        }}
                    >
                        <div
                            style={{
                                padding: 18,
                                border: "1px solid #e2e8f0",
                                borderRadius: 12,
                            }}
                        >
                            <div style={{ color: "#64748b" }}>
                                Total
                            </div>
                            <strong>{data.total}</strong>
                        </div>

                        <div
                            style={{
                                padding: 18,
                                border: "1px solid #e2e8f0",
                                borderRadius: 12,
                            }}
                        >
                            <div style={{ color: "#64748b" }}>
                                PDF Available
                            </div>
                            <strong>{data.pdf_available}</strong>
                        </div>

                        <div
                            style={{
                                padding: 18,
                                border: "1px solid #e2e8f0",
                                borderRadius: 12,
                            }}
                        >
                            <div style={{ color: "#64748b" }}>
                                Metadata Only
                            </div>
                            <strong>{data.pdf_missing}</strong>
                        </div>
                    </div>

                    <div
                        style={{
                            display: "flex",
                            flexDirection: "column",
                            gap: 8,
                        }}
                    >
                        {data.items.slice(0, 100).map((item) => (
                            <div
                                key={item.id}
                                style={{
                                    padding: 16,
                                    border:
                                        "1px solid #e2e8f0",
                                    borderRadius: 10,
                                }}
                            >
                                <div
                                    style={{
                                        fontWeight: 600,
                                        marginBottom: 6,
                                    }}
                                >
                                    {item.title}
                                </div>

                                <div
                                    style={{
                                        fontSize: 13,
                                        color: "#64748b",
                                    }}
                                >
                                    {item.status}
                                </div>
                            </div>
                        ))}
                    </div>
                </>
            )}
        </main>
        </WorkspaceShell>
    );
}
