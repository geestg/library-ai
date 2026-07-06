import {
  BrainCircuit,
  Sparkles,
  BookOpen,
  CheckCircle2
} from "lucide-react";

export default function ResearchSummaryCard({

  researchProfile,

  sourceCount = 0

}) {

  const novelty =

    researchProfile?.novelty || {};

  const prodi =

    researchProfile?.prodi || {};

  const noveltyScore =

    novelty.novelty_score ?? "-";

  const researchDomain =

    prodi.prodi ||

    "General Research";

  const hasEvidence =

    sourceCount > 0;

  return (

    <div className="research-summary-card">

      {/* ========================= */}
      {/* HEADER */}
      {/* ========================= */}

      <div className="research-summary-header">

        <div className="research-summary-badge">

          <BrainCircuit size={14} />

          Research Intelligence

        </div>

        <h2>

          Current Research Session

        </h2>

      </div>

      {/* ========================= */}
      {/* GRID */}
      {/* ========================= */}

      <div className="research-summary-grid">

        <div className="summary-item">

          <BrainCircuit size={18} />

          <div>

            <span>

              Research Profile

            </span>

            <strong>

              {researchDomain}

            </strong>

          </div>

        </div>

        <div className="summary-item">

          <Sparkles size={18} />

          <div>

            <span>

              Novelty

            </span>

            <strong>

              {noveltyScore}/10

            </strong>

          </div>

        </div>

        <div className="summary-item">

          <BookOpen size={18} />

          <div>

            <span>

              Related Thesis

            </span>

            <strong>

              {sourceCount}

            </strong>

          </div>

        </div>

        <div className="summary-item">

          <CheckCircle2 size={18} />

          <div>

            <span>

              Research Status

            </span>

            <strong>

              {

                hasEvidence

                ? "Evidence Ready"

                : "Waiting"

              }

            </strong>

          </div>

        </div>

      </div>

    </div>

  );

}