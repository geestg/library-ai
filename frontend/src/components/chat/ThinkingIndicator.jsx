import { BrainCircuit } from "lucide-react";

export default function ThinkingIndicator() {
  return (
    <div className="message assistant loading-indicator" style={{ marginBottom: "16px" }}>
      <div className="assistant-avatar-header">
        <div className="assistant-mini-avatar">
          <BrainCircuit size={14} color="#ffffff" />
        </div>
        <div className="assistant-title-meta">
          <span className="assistant-name">DELBot</span>
        </div>
      </div>

      <div className="thinking-dots-simple">
        <span className="dot">.</span>
        <span className="dot">.</span>
        <span className="dot">.</span>
      </div>
    </div>
  );
}