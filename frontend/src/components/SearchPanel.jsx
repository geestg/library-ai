import {
  useEffect
} from "react";

import {
  FileText,
  Sparkles,
  ExternalLink
} from "lucide-react";

export default function SearchPanel({

  sources = [],

  evidence = {},

  activeCitation,

  setActiveCitation,

  selectedThesis,

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

            Citation-aware retrieval evidence
            from DELBot research pipeline.

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

              evidence.technologies?.length > 0 && (

                <div className="summary-group">

                  <h4>

                    Technologies

                  </h4>

                  <div>

                    {

                      evidence.technologies.map(

                        (
                          item,
                          idx
                        ) => (

                          <div
                            key={idx}
                            className="summary-pill"
                          >

                            {item.name}

                            {" "}

                            ({item.count})

                          </div>

                        )
                      )

                    }

                  </div>

                </div>

              )

            }

            {

              evidence.methods?.length > 0 && (

                <div className="summary-group">

                  <h4>

                    Methods

                  </h4>

                  <div>

                    {

                      evidence.methods.map(

                        (
                          item,
                          idx
                        ) => (

                          <div
                            key={idx}
                            className="summary-pill"
                          >

                            {item.name}

                            {" "}

                            ({item.count})

                          </div>

                        )
                      )

                    }

                  </div>

                </div>

              )

            }

            {

              evidence.domains?.length > 0 && (

                <div className="summary-group">

                  <h4>

                    Domains

                  </h4>

                  <div>

                    {

                      evidence.domains.map(

                        (
                          item,
                          idx
                        ) => (

                          <div
                            key={idx}
                            className="summary-pill"
                          >

                            {item.name}

                            {" "}

                            ({item.count})

                          </div>

                        )
                      )

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

                onClick={() =>
                  setSelectedThesis(
                    source
                  )
                }

               className={`evidence-card ${
                isActive
                  ? "active"
                  : ""
              }`}

              style={{
                cursor: "pointer"
              }}

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

                {/* ===================== */}
                {/* AUTHOR */}
                {/* ===================== */}

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

                {/* ===================== */}
                {/* YEAR + PRODI */}
                {/* ===================== */}

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

                {/* ===================== */}
                {/* SCORE */}
                {/* ===================== */}

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

                {/* ===================== */}
                {/* REPOSITORY */}
                {/* ===================== */}

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