import { Upload } from "lucide-react";
import type { CSSProperties } from "react";

const topbar: CSSProperties = {
    minHeight: 58,
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "0 24px",
    background: "#ffffff",
    borderBottom: "1px solid #e5e7eb",
};

const title: CSSProperties = {
    fontSize: 14,
    fontWeight: 600,
    color: "#0f172a",
};

const subtitle: CSSProperties = {
    marginTop: 2,
    fontSize: 11,
    color: "#94a3b8",
};

const button: CSSProperties = {
    display: "inline-flex",
    alignItems: "center",
    gap: 7,
    minHeight: 34,
    padding: "0 13px",
    border: "1px solid #2563eb",
    borderRadius: 7,
    background: "#2563eb",
    color: "#ffffff",
    fontSize: 12,
    fontWeight: 600,
};

export default function WorkspaceTopbar() {
    return (
        <header style={topbar}>
            <div>
                <div style={title}>
                    Academic Research Workspace
                </div>

                <div style={subtitle}>
                    Explore documents, literature, and research evidence
                </div>
            </div>

            <button type="button" style={button}>
                <Upload
                    width={15}
                    height={15}
                    strokeWidth={2}
                />
                Import Repository
            </button>
        </header>
    );
}
