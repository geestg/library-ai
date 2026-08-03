import {
    Settings,
    Server,
    Database,
    BrainCircuit,
    ShieldCheck,
    Construction,
} from "lucide-react";

export default function SettingsPage() {

    const card: React.CSSProperties = {
        background: "#ffffff",
        border: "1px solid #e5e7eb",
        borderRadius: 12,
        padding: 24,
        boxShadow: "0 1px 4px rgba(0,0,0,.05)",
    };

    const row: React.CSSProperties = {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "14px 0",
        borderTop: "1px solid #f1f5f9",
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
                <Settings size={34} />
                <div>
                    <h1 style={{ margin: 0 }}>
                        Settings
                    </h1>
                    <div
                        style={{
                            color: "#64748b",
                            marginTop: 4,
                        }}
                    >
                        DELBot MVP Configuration
                    </div>
                </div>
            </div>

            <div
                style={{
                    ...card,
                    marginBottom: 24,
                    display: "flex",
                    gap: 12,
                    alignItems: "center",
                    background: "#fff7ed",
                    border: "1px solid #fed7aa",
                }}
            >
                <Construction
                    size={22}
                    color="#ea580c"
                />

                <div>
                    <strong>
                        Configuration UI is not available yet.
                    </strong>

                    <div
                        style={{
                            marginTop: 6,
                            color: "#9a3412",
                        }}
                    >
                        Backend configuration endpoints have not been
                        implemented in the MVP.
                    </div>
                </div>

            </div>

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns:
                        "repeat(auto-fit,minmax(320px,1fr))",
                    gap: 20,
                }}
            >

                <div style={card}>

                    <h2
                        style={{
                            marginTop: 0,
                            display: "flex",
                            alignItems: "center",
                            gap: 10,
                        }}
                    >
                        <Server size={20} />
                        Backend
                    </h2>

                    <div style={row}>
                        <span>Gateway</span>
                        <strong>READY</strong>
                    </div>

                    <div style={row}>
                        <span>Repository API</span>
                        <strong>READY</strong>
                    </div>

                    <div style={row}>
                        <span>Research API</span>
                        <strong>READY</strong>
                    </div>

                    <div style={row}>
                        <span>Settings API</span>
                        <strong>NOT AVAILABLE</strong>
                    </div>

                </div>

                <div style={card}>

                    <h2
                        style={{
                            marginTop: 0,
                            display: "flex",
                            alignItems: "center",
                            gap: 10,
                        }}
                    >
                        <Database size={20} />
                        Repository
                    </h2>

                    <div style={row}>
                        <span>Repository Explorer</span>
                        <strong>READY</strong>
                    </div>

                    <div style={row}>
                        <span>Document Index</span>
                        <strong>READY</strong>
                    </div>

                    <div style={row}>
                        <span>Semantic Search</span>
                        <strong>PLACEHOLDER</strong>
                    </div>

                </div>

                <div style={card}>

                    <h2
                        style={{
                            marginTop: 0,
                            display: "flex",
                            alignItems: "center",
                            gap: 10,
                        }}
                    >
                        <BrainCircuit size={20} />
                        AI Services
                    </h2>

                    <div style={row}>
                        <span>Research Pipeline</span>
                        <strong>READY</strong>
                    </div>

                    <div style={row}>
                        <span>Citation Builder</span>
                        <strong>READY</strong>
                    </div>

                    <div style={row}>
                        <span>Semantic Search API</span>
                        <strong>NOT AVAILABLE</strong>
                    </div>

                </div>

                <div style={card}>

                    <h2
                        style={{
                            marginTop: 0,
                            display: "flex",
                            alignItems: "center",
                            gap: 10,
                        }}
                    >
                        <ShieldCheck size={20} />
                        MVP Status
                    </h2>

                    <div style={row}>
                        <span>Dashboard</span>
                        <strong>PASS</strong>
                    </div>

                    <div style={row}>
                        <span>Repository</span>
                        <strong>PASS</strong>
                    </div>

                    <div style={row}>
                        <span>Documents</span>
                        <strong>PASS</strong>
                    </div>

                    <div style={row}>
                        <span>Research</span>
                        <strong>PASS</strong>
                    </div>

                    <div style={row}>
                        <span>Frontend Build</span>
                        <strong>PASS</strong>
                    </div>

                </div>

            </div>

        </div>

    );

}
