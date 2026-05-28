import {
  Sparkles,
  BrainCircuit,
  FlaskConical,
  FileText
} from "lucide-react";

export default function ChatHero({

  setInput

}) {

  return (

    <div className="hero-section">

      {/* ========================= */}
      {/* HERO BADGE */}
      {/* ========================= */}

      <div className="hero-badge">

        <Sparkles size={14} />

        DELBot Academic Intelligence

      </div>

      {/* ========================= */}
      {/* HERO TITLE */}
      {/* ========================= */}

      <h1>

        Research smarter,
        not harder.

      </h1>

      {/* ========================= */}
      {/* HERO SUBTITLE */}
      {/* ========================= */}

      <p>

        AI-native academic workspace
        for literature review,
        semantic retrieval,
        citation-aware answering,
        and research synthesis.

      </p>

      {/* ========================= */}
      {/* MINI STATS */}
      {/* ========================= */}

      <div className="hero-mini-stats">

        <div className="hero-stat">

          <strong>
            Hybrid RAG
          </strong>

          <span>
            BM25 + Vector Search
          </span>

        </div>

        <div className="hero-stat">

          <strong>
            Evidence Aware
          </strong>

          <span>
            Citation Grounded Answers
          </span>

        </div>

        <div className="hero-stat">

          <strong>
            Academic AI
          </strong>

          <span>
            Research Intelligence System
          </span>

        </div>

      </div>

      {/* ========================= */}
      {/* HERO GRID */}
      {/* ========================= */}

      <div className="hero-grid">

        <div
          className="hero-card"
          onClick={() =>
            setInput(
              "Cari research gap NLP healthcare"
            )
          }
        >

          <BrainCircuit size={22} />

          <h3>
            Research Gap
          </h3>

          <span>
            Identifikasi peluang novelty penelitian
          </span>

        </div>

        <div
          className="hero-card"
          onClick={() =>
            setInput(
              "Generate ide judul skripsi AI"
            )
          }
        >

          <FlaskConical size={22} />

          <h3>
            Thesis Ideas
          </h3>

          <span>
            Generate topik skripsi modern
          </span>

        </div>

        <div
          className="hero-card"
          onClick={() =>
            setInput(
              "Ringkas paper transformer terbaru"
            )
          }
        >

          <FileText size={22} />

          <h3>
            Paper Summary
          </h3>

          <span>
            Summarize dan ekstrak insight
          </span>

        </div>

      </div>

    </div>
  );
}