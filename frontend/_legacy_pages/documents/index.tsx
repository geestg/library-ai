import { useState } from "react";
import {
    Database,
    Play,
    Loader2,
    CheckCircle2,
    FileText,
    SkipForward,
} from "lucide-react";
import { indexRepository } from "../../api/document";

type IndexResult = {
    success: boolean;
    indexed: number;
    skipped: number;
    total_pdf: number;
};

export default function DocumentsPage() {

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [result, setResult] = useState<IndexResult | null>(null);

    async function runIndex() {

        setLoading(true);
        setError("");
        setResult(null);

        try {

            const response = await indexRepository();

            setResult(response.data);

        } catch (err: any) {

            setError(err?.message ?? "Index failed.");

        } finally {

            setLoading(false);

        }

    }

    const card: React.CSSProperties = {
        background: "#ffffff",
        border: "1px solid #e5e7eb",
        borderRadius: 12,
        padding: 24,
        boxShadow: "0 1px 4px rgba(0,0,0,.05)",
    };

    const stat: React.CSSProperties = {
        ...card,
        flex: 1,
        minWidth: 180,
    };

    return (

        <div>

            <div
                style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 12,
                    marginBottom: 24,
                }}
            >
                <Database size={30} />

                <div>

                    <h1
                        style={{
                            margin: 0,
                            fontSize: 30,
                        }}
                    >
                        Document Index
                    </h1>

                    <p
                        style={{
                            marginTop: 6,
                            color: "#6b7280",
                        }}
                    >
                        Build Knowledge Base from repository PDFs.
                    </p>

                </div>

            </div>

            <div style={card}>

                <button
                    onClick={runIndex}
                    disabled={loading}
                    style={{
                        display: "flex",
                        alignItems: "center",
                        gap: 10,
                        padding: "12px 20px",
                        border: "none",
                        borderRadius: 10,
                        background: "#2563eb",
                        color: "#fff",
                        fontWeight: 600,
                        cursor: loading ? "default" : "pointer",
                    }}
                >

                    {loading
                        ? <Loader2 size={18} />
                        : <Play size={18} />}

                    {loading
                        ? "Indexing..."
                        : "Start Index"}

                </button>

                {error && (

                    <div
                        style={{
                            marginTop: 18,
                            color: "#dc2626",
                        }}
                    >
                        {error}
                    </div>

                )}

            </div>

            {result && (

                <div
                    style={{
                        display: "flex",
                        gap: 18,
                        flexWrap: "wrap",
                        marginTop: 24,
                    }}
                >

                    <div style={stat}>
                        <CheckCircle2 size={22} />
                        <h2>{String(result.success)}</h2>
                        <div>Status</div>
                    </div>

                    <div style={stat}>
                        <FileText size={22} />
                        <h2>{result.indexed}</h2>
                        <div>Indexed</div>
                    </div>

                    <div style={stat}>
                        <SkipForward size={22} />
                        <h2>{result.skipped}</h2>
                        <div>Skipped</div>
                    </div>

                    <div style={stat}>
                        <Database size={22} />
                        <h2>{result.total_pdf}</h2>
                        <div>Total PDF</div>
                    </div>

                </div>

            )}

        </div>

    );

}
