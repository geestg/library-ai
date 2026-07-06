import {
  BrainCircuit
} from "lucide-react";

export default function ChatHero() {

  return (

    <div className="hero-section">

      {/* ========================= */}
      {/* BRAND */}
      {/* ========================= */}

      <div className="hero-badge">

        <BrainCircuit size={14} />

        DELBot

      </div>

      {/* ========================= */}
      {/* TITLE */}
      {/* ========================= */}

      <h1>

        Academic Research Intelligence

      </h1>

      {/* ========================= */}
      {/* DESCRIPTION */}
      {/* ========================= */}

      <p>

        Research starts with a question.

      </p>

      {/* ========================= */}
      {/* CAPABILITIES */}
      {/* ========================= */}

      <div className="hero-description">

        DELBot automatically understands your research intent,
        retrieves relevant academic evidence, analyzes research
        trends, identifies research gaps, compares methodologies,
        understands uploaded documents, and generates grounded
        research recommendations without requiring you to choose
        specific tools.

      </div>

    </div>

  );

}