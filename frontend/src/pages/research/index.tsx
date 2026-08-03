import { Link } from "react-router-dom";
import {
    BrainCircuit,
    ArrowLeft,
    Sparkles,
} from "lucide-react";

export default function ResearchPage() {

    const card: React.CSSProperties = {
        background: "#ffffff",
        border: "1px solid #e5e7eb",
        borderRadius: 16,
        padding: 32,
        boxShadow: "0 2px 8px rgba(15,23,42,.05)",
    };

    return (

        <div
            style={{
                maxWidth: 900,
                margin: "0 auto",
            }}
        >

            <div style={card}>

                <div
                    style={{
                        display: "flex",
                        alignItems: "center",
                        gap: 12,
                        marginBottom: 24,
                    }}
                >

                    <BrainCircuit
                        size={32}
                        color="#2563eb"
                    />

                    <h1
                        style={{
                            margin: 0,
                        }}
                    >
                        AI Research Workspace
                    </h1>

                </div>

                <p
                    style={{
                        lineHeight: 1.9,
                        color: "#64748b",
                        marginBottom: 32,
                    }}
                >
                    DELBot now starts every research session directly
                    from the AI Workspace on the Dashboard.
                    Conversation, evidence retrieval, citations,
                    and repository reasoning are unified into
                    a single workspace experience.
                </p>

                <div
                    style={{
                        padding: 24,
                        borderRadius: 12,
                        background: "#f8fafc",
                        border: "1px solid #e5e7eb",
                        marginBottom: 32,
                    }}
                >

                    <div
                        style={{
                            display: "flex",
                            alignItems: "center",
                            gap: 10,
                            marginBottom: 12,
                        }}
                    >

                        <Sparkles
                            size={20}
                            color="#2563eb"
                        />

                        <strong>
                            Research now begins from Dashboard
                        </strong>

                    </div>

                    <div
                        style={{
                            lineHeight: 1.8,
                            color: "#64748b",
                        }}
                    >
                        • AI Conversation

                        <br />

                        • Repository Evidence

                        <br />

                        • Citation Panel

                        <br />

                        • Workspace Memory

                        <br />

                        • Research Timeline

                    </div>

                </div>

                <Link
                    to="/"
                    style={{
                        display: "inline-flex",
                        alignItems: "center",
                        gap: 10,
                        padding: "14px 22px",
                        borderRadius: 12,
                        background: "#2563eb",
                        color: "#ffffff",
                        textDecoration: "none",
                        fontWeight: 700,
                    }}
                >

                    <ArrowLeft size={18} />

                    Return to AI Workspace

                </Link>

            </div>

        </div>

    );

}