import {
  FileText,
  Calendar,
  GraduationCap,
  ChevronRight
} from "lucide-react";

export default function RelatedThesisWidget({

  sources = [],

  activeCitation,

  setActiveCitation,

  setSelectedThesis

}) {

  return (

    <div className="research-widget">

      {/* ========================= */}
      {/* HEADER */}
      {/* ========================= */}

      <div className="research-widget-header">

        <div className="research-widget-title">

          <FileText size={16} />

          Retrieved Evidence

        </div>

      </div>

      {

        sources.length === 0 && (

          <div className="research-empty">

            No academic evidence retrieved.

          </div>

        )

      }

      {

        sources.map((source) => {

          const active =

            activeCitation ===

            source.source_id;

          return (

            <div

              key={source.source_id}

              className={

                `research-source-card ${
                  active
                  ? "active"
                  : ""
                }`

              }

              onClick={() => {

                setActiveCitation?.(

                  source.source_id

                );

                setSelectedThesis?.(

                  source

                );

              }}

            >

              {/* ===================== */}

              <div className="research-source-top">

                <div className="research-source-title">

                  {

                    source.title ||

                    "Untitled Thesis"

                  }

                </div>

                <ChevronRight

                  size={16}

                />

              </div>

              {/* ===================== */}

              <div className="research-source-meta">

                <span>

                  <Calendar size={13}/>

                  {

                    source.year ||

                    "-"

                  }

                </span>

                <span>

                  <GraduationCap

                    size={13}

                  />

                  {

                    source.prodi ||

                    "-"

                  }

                </span>

              </div>

              {/* ===================== */}

              <div className="research-score">

                <div className="research-score-header">

                  <span>

                    Relevance

                  </span>

                  <strong>

                    {

                      Number(

                        source.score || 0

                      ).toFixed(2)

                    }

                  </strong>

                </div>

                <div className="research-score-bar">

                  <div

                    className="research-score-fill"

                    style={{

                      width:

                      `${Math.min(

                        source.score * 10,

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

  );

}