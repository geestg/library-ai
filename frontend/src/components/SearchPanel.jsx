import {
  FileText,
  Hash,
  Layers3,
  Sparkles
} from "lucide-react";

export default function SearchPanel({

  sources = [],

  activeCitation

}) {

  return (

    <div className="evidence-shell">

      {/* ============================= */}
      {/* HEADER */}
      {/* ============================= */}

      <div className="evidence-header">

        <div>

          <div className="evidence-badge">

            <Sparkles size={13} />

            Evidence Engine

          </div>

          <h2>
            Academic Sources
          </h2>

          <p>
            Citation-aware retrieval evidence
            from DELBot RAG pipeline.
          </p>

        </div>

      </div>

      {/* ============================= */}
      {/* EMPTY */}
      {/* ============================= */}

      {

        sources.length === 0 && (

          <div className="evidence-empty">

            <div className="empty-icon">

              <FileText size={34} />

            </div>

            <h3>
              No evidence yet
            </h3>

            <p>

              Upload academic documents and
              ask research questions to see
              retrieval evidence.

            </p>

          </div>
        )
      }

      {/* ============================= */}
      {/* SOURCE LIST */}
      {/* ============================= */}

      <div className="evidence-list">

        {

          sources.map((source) => {

            const isActive =

              activeCitation ===
              source.source_id;

            return (

              <div

                key={source.source_id}

                className={`evidence-card ${
                  isActive
                    ? "active"
                    : ""
                }`}
              >

                {/* ===================== */}
                {/* TOP */}
                {/* ===================== */}

                <div className="evidence-card-top">

                  <div className="evidence-source-icon">

                    <FileText size={18} />

                  </div>

                  <div className="evidence-top-content">

                    <div className="evidence-source-name">

                      {

                        source.source_file ||
                        "Unknown Document"
                      }

                    </div>

                    <div className="evidence-citation-id">

                      Citation
                      {" "}
                      [{source.source_id}]
                    </div>

                  </div>

                </div>

                {/* ===================== */}
                {/* META */}
                {/* ===================== */}

                <div className="evidence-meta-grid">

                  <div className="meta-pill">

                    <Hash size={12} />

                    Page
                    {" "}
                    {source.page || "-"}

                  </div>

                  <div className="meta-pill">

                    <Layers3 size={12} />

                    Chunk
                    {" "}
                    {source.chunk_index || "-"}

                  </div>

                </div>

                {/* ===================== */}
                {/* SCORE */}
                {/* ===================== */}

                <div className="evidence-score-wrapper">

                  <div className="score-header">

                    <span>
                      Relevance
                    </span>

                    <span>

                      {Number(
                        source.score || 0
                      ).toFixed(2)}

                    </span>

                  </div>

                  <div className="score-bar">

                    <div

                      className="score-fill"

                      style={{

                        width: `${Math.min(
                          (source.score || 0) * 100,
                          100
                        )}%`
                      }}
                    />

                  </div>

                </div>

              </div>
            );
          })
        }

      </div>

    </div>
  );
}