import { useEffect } from "react";

import {
  FileText,
  Sparkles,
  ExternalLink,
  BarChart3
} from "lucide-react";

export default function SearchPanel({

  sources = [],

  evidence = {},

  evidenceMatrix = {},

  gapAnalysis = {},

  activeCitation,

  setActiveCitation,

  setSelectedThesis

}) {

  // =================================
  // ACTIVE CITATION SCROLL
  // =================================

  useEffect(() => {

    if (!activeCitation) {
      return;
    }

    const container =
      document.querySelector(
        ".evidence-shell"
      );

    const element =
      document.getElementById(
        `citation-${activeCitation}`
      );

    if (
      !container ||
      !element
    ) {
      return;
    }

    const containerRect =
      container.getBoundingClientRect();

    const elementRect =
      element.getBoundingClientRect();

    const targetScrollTop =
      elementRect.top -
      containerRect.top +
      container.scrollTop -
      120;

    container.scrollTo({

      top: targetScrollTop,

      behavior: "smooth"

    });

  }, [activeCitation]);

  // =================================
  // SUMMARY GROUP
  // =================================

  const renderSummaryGroup = (
    title,
    items
  ) => {

    if (
      !items ||
      items.length === 0
    ) {
      return null;
    }

    return (

      <div className="summary-group">

        <h4>
          {title}
        </h4>

        <div>

          {

            items.map(

              (
                item,
                idx
              ) => (

                <div

                  key={`${title}-${idx}`}

                  className="summary-pill"

                >

                  {

                    item.name
                    ?? item.year
                    ?? item

                  }

                  {

                    item.count !== undefined && (
                      <>
                        {" "}
                        ({item.count})
                      </>
                    )

                  }

                </div>

              )

            )

          }

        </div>

      </div>

    );

  };

  // =================================
  // MATRIX GROUP
  // =================================

  const renderMatrixGroup = (
    title,
    matrixData
  ) => {

    if (
      !matrixData ||
      Object.keys(matrixData)
        .length === 0
    ) {
      return null;
    }

    return (

      <div className="summary-group">

        <h4>
          {title}
        </h4>

        <div>

          {

            Object.entries(
              matrixData
            ).map(

              (
                [name, count]
              ) => (

                <div

                  key={name}

                  className="summary-pill"

                >

                  {name}
                  {" "}
                  ({count})

                </div>

              )

            )

          }

        </div>

      </div>

    );

  };

  // =================================
  // GAP SECTION
  // =================================

  const renderGapSection = (
    title,
    items,
    className = "gap-item"
  ) => {

    if (
      !items ||
      items.length === 0
    ) {
      return null;
    }

    return (

      <div className="summary-group">

        <h4>
          {title}
        </h4>

        <div>

          {

            items.map(

              (
                item,
                idx
              ) => (

                <div

                  key={`${title}-${idx}`}

                  className={className}

                >

                  {item}

                </div>

              )

            )

          }

        </div>

      </div>

    );

  };

  return (

    <div className="evidence-shell">

      {/* ================================= */}
      {/* HEADER */}
      {/* ================================= */}

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

            Citation-aware retrieval
            evidence from DELBot
            research intelligence engine.

          </p>

        </div>

      </div>

      {/* ================================= */}
      {/* EVIDENCE SUMMARY */}
      {/* ================================= */}

      {

        Object.keys(
          evidence || {}
        ).length > 0 && (

          <div className="evidence-summary">

            <h3>

              Evidence Summary

            </h3>

            {

              renderSummaryGroup(
                "Technologies",
                evidence.technologies
              )

            }

            {

              renderSummaryGroup(
                "Methodologies",
                evidence.methodologies
              )

            }

            {

              renderSummaryGroup(
                "Research Domains",
                evidence.research_domains
              )

            }

            {

              renderSummaryGroup(
                "Datasets",
                evidence.datasets
              )

            }

            {

              renderSummaryGroup(
                "Evaluation Metrics",
                evidence.evaluation_metrics
              )

            }

            {

              renderSummaryGroup(
                "Research Years",
                evidence.years
              )

            }

          </div>

        )

      }

      {/* ================================= */}
      {/* EVIDENCE MATRIX */}
      {/* ================================= */}

      {

        Object.keys(
          evidenceMatrix || {}
        ).length > 0 && (

          <div className="evidence-summary">

            <h3>

              <BarChart3
                size={16}
                style={{
                  marginRight: 8
                }}
              />

              Evidence Matrix

            </h3>

            {

              renderMatrixGroup(
                "Technology Frequency",
                evidenceMatrix.technology_frequency
              )

            }

            {

              renderMatrixGroup(
                "Methodology Frequency",
                evidenceMatrix.methodology_frequency
              )

            }

            {

              renderMatrixGroup(
                "Domain Frequency",
                evidenceMatrix.domain_frequency
              )

            }

            {

              renderMatrixGroup(
                "Dataset Frequency",
                evidenceMatrix.dataset_frequency
              )

            }

            {

              renderMatrixGroup(
                "Evaluation Frequency",
                evidenceMatrix.evaluation_frequency
              )

            }

            {

              renderMatrixGroup(
                "Year Frequency",
                evidenceMatrix.year_frequency
              )

            }

          </div>

        )

      }

      {/* ================================= */}
      {/* GAP ANALYSIS */}
      {/* ================================= */}

      {

        Object.keys(
          gapAnalysis || {}
        ).length > 0 && (

          <div className="gap-section">

            <h3>

              Research Gap Analysis

            </h3>

            {

              renderGapSection(
                "Method Gap",
                gapAnalysis.method_gap
              )

            }

            {

              renderGapSection(
                "Dataset Gap",
                gapAnalysis.dataset_gap
              )

            }

            {

              renderGapSection(
                "Temporal Gap",
                gapAnalysis.temporal_gap
              )

            }

            {

              renderGapSection(
                "Evaluation Gap",
                gapAnalysis.evaluation_gap
              )

            }

            {

              renderGapSection(
                "Novelty Opportunities",
                gapAnalysis.novelty_opportunities,
                "novelty-item"
              )

            }

            {

              gapAnalysis.gap_score !==
              undefined && (

                <div className="summary-group">

                  <h4>

                    Gap Score

                  </h4>

                  <div className="gap-score">

                    {

                      gapAnalysis.gap_score

                    }

                  </div>

                </div>

              )

            }

          </div>

        )

      }

      {/* ================================= */}
      {/* EMPTY STATE */}
      {/* ================================= */}

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

              Ask a research question and
              DELBot will display retrieved
              thesis evidence here.

            </p>

          </div>

        )

      }

      {/* ================================= */}
      {/* SOURCE LIST */}
      {/* ================================= */}

      <div className="evidence-list">

        {

          sources.map((source) => {

            const isActive =

              activeCitation ===
              source.source_id;

            return (

              <div

                id={
                  `citation-${source.source_id}`
                }

                key={source.source_id}

                onClick={() => {

                  setActiveCitation?.(
                    source.source_id
                  );

                  setSelectedThesis?.(
                    source
                  );

                }}

                className={`evidence-card ${
                  isActive
                    ? "active"
                    : ""
                }`}

                style={{
                  cursor: "pointer"
                }}

              >

                <div className="evidence-card-top">

                  <div className="evidence-source-icon">

                    <FileText size={18} />

                  </div>

                  <div className="evidence-top-content">

                    <div className="evidence-source-name">

                      {

                        source.title ||

                        "Unknown Thesis"

                      }

                    </div>

                    <div className="evidence-citation-id">

                      Citation #

                      {source.source_id}

                    </div>

                  </div>

                </div>

                <div
                  style={{
                    marginTop: "14px",
                    color:
                      "rgba(255,255,255,0.7)",
                    fontSize: "13px"
                  }}
                >

                  {

                    source.author ||

                    "Unknown Author"

                  }

                </div>

                <div
                  style={{
                    marginTop: "10px",
                    display: "flex",
                    gap: "10px",
                    flexWrap: "wrap"
                  }}
                >

                  <div className="meta-pill">

                    Year:

                    {" "}

                    {

                      source.year ||

                      "-"

                    }

                  </div>

                  <div className="meta-pill">

                    {

                      source.prodi ||

                      "-"

                    }

                  </div>

                </div>

                <div className="evidence-score-wrapper">

                  <div className="score-header">

                    <span>

                      Relevance

                    </span>

                    <span>

                      {

                        Number(
                          source.score || 0
                        ).toFixed(2)

                      }

                    </span>

                  </div>

                  <div className="score-bar">

                    <div

                      className="score-fill"

                      style={{

                        width: `${Math.min(
                          (source.score || 0) * 10,
                          100
                        )}%`

                      }}

                    />

                  </div>

                </div>

                {

                  source.url && (

                    <a

                      href={source.url}

                      target="_blank"

                      rel="noopener noreferrer"

                      className="evidence-link"

                      onClick={(e) =>
                        e.stopPropagation()
                      }

                    >

                      <ExternalLink
                        size={14}
                      />

                      Open Repository

                    </a>

                  )

                }

              </div>

            );

          })

        }

      </div>

    </div>

  );

}