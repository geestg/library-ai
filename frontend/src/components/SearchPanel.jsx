import {
  useEffect,
} from "react";

import {
  ExternalLink,
} from "lucide-react";

export default function SearchPanel({

  sources = [],

  activeCitation,

  setActiveCitation,

  setSelectedThesis,

}) {

  // =====================================
  // SOURCE STATE
  // =====================================

  const hasSources =
    sources.length > 0;

  // =====================================
  // ACTIVE CITATION SCROLL
  // =====================================

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

      92;

    container.scrollTo({

      top:
        targetScrollTop,

      behavior:
        "smooth",

    });

  }, [

    activeCitation,

  ]);

  // =====================================
  // SELECT SOURCE
  // =====================================

  const selectSource =
    (source) => {

      setActiveCitation?.(
        source.source_id
      );

      setSelectedThesis?.(
        source
      );

    };

  // =====================================
  // KEYBOARD INTERACTION
  // =====================================

  const handleSourceKeyDown =
    (

      event,

      source

    ) => {

      if (

        event.key !== "Enter" &&

        event.key !== " "

      ) {

        return;

      }

      event.preventDefault();

      selectSource(
        source
      );

    };

  // =====================================
  // SCORE
  // =====================================

  const getScoreData =
    (score) => {

      const numericScore =
        Number(score || 0);

      const percentage =

        numericScore <= 1

          ? numericScore * 100

          : numericScore <= 10

            ? numericScore * 10

            : numericScore;

      const safePercentage =
        Math.max(

          0,

          Math.min(
            percentage,
            100
          )

        );

      return {

        percentage:
          safePercentage,

        label:
          `${Math.round(
            safePercentage
          )}%`,

      };

    };

  // =====================================
  // UI
  // =====================================

  return (

    <aside

      className="evidence-shell"

      aria-label="Sumber akademik"

    >

      {/* ================================= */}
      {/* HEADER */}
      {/* ================================= */}

      <header className="evidence-header">

        <div className="evidence-heading-row">

          <h2>

            Sumber

          </h2>

          {

            hasSources && (

              <span className="evidence-count">

                {sources.length}

              </span>

            )

          }

        </div>

        <p>

          Bukti akademik yang mendukung jawaban.

        </p>

      </header>

      {/* ================================= */}
      {/* EMPTY STATE */}
      {/* ================================= */}

      {

        !hasSources ? (

          <div className="evidence-empty">

            <div

              className="evidence-empty-mark"

              aria-hidden="true"

            >

              <span />

              <span />

              <span />

            </div>

            <h3>

              Belum ada sumber

            </h3>

            <p>

              Sumber yang relevan akan muncul
              di sini setelah pencarian akademik.

            </p>

          </div>

        ) : (

          /* ================================= */
          /* SOURCE LIST */
          /* ================================= */

          <div className="evidence-list">

            {

              sources.map(

                (

                  source,

                  index

                ) => {

                  const isActive =

                    activeCitation ===
                    source.source_id;

                  const score =
                    getScoreData(
                      source.score
                    );

                  return (

                    <article

                      id={
                        `citation-${source.source_id}`
                      }

                      key={
                        source.source_id
                      }

                      className={

                        `evidence-card${
                          isActive
                            ? " active"
                            : ""
                        }`

                      }

                      role="button"

                      tabIndex={0}

                      aria-pressed={
                        isActive
                      }

                      onClick={() =>

                        selectSource(
                          source
                        )

                      }

                      onKeyDown={

                        (event) =>

                          handleSourceKeyDown(

                            event,

                            source

                          )

                      }

                    >

                      {/* ===================== */}
                      {/* SOURCE NUMBER */}
                      {/* ===================== */}

                      <div className="evidence-source-index">

                        {

                          index + 1

                        }

                      </div>

                      {/* ===================== */}
                      {/* SOURCE CONTENT */}
                      {/* ===================== */}

                      <div className="evidence-card-content">

                        <h3 className="evidence-source-name">

                          {

                            source.title ||

                            "Judul tidak tersedia"

                          }

                        </h3>

                        <div className="evidence-source-meta">

                          <span>

                            {

                              source.author ||

                              "Penulis tidak tersedia"

                            }

                          </span>

                          {

                            source.year && (

                              <>

                                <span

                                  className="evidence-meta-separator"

                                  aria-hidden="true"

                                />

                                <span>

                                  {source.year}

                                </span>

                              </>

                            )

                          }

                          {

                            source.prodi && (

                              <>

                                <span

                                  className="evidence-meta-separator"

                                  aria-hidden="true"

                                />

                                <span>

                                  {source.prodi}

                                </span>

                              </>

                            )

                          }

                        </div>

                        {/* =================== */}
                        {/* RELEVANCE */}
                        {/* =================== */}

                        <div className="evidence-score-wrapper">

                          <div className="score-header">

                            <span>

                              Relevansi

                            </span>

                            <span>

                              {score.label}

                            </span>

                          </div>

                          <div

                            className="score-bar"

                            aria-hidden="true"

                          >

                            <div

                              className="score-fill"

                              style={{

                                width:
                                  `${score.percentage}%`,

                              }}

                            />

                          </div>

                        </div>

                        {/* =================== */}
                        {/* REPOSITORY */}
                        {/* =================== */}

                        {

                          source.url && (

                            <a

                              href={
                                source.url
                              }

                              target="_blank"

                              rel="noopener noreferrer"

                              className="evidence-link"

                              onClick={

                                (event) =>

                                  event.stopPropagation()

                              }

                            >

                              <span>

                                Buka repositori

                              </span>

                              <ExternalLink

                                size={13}

                                strokeWidth={2}

                              />

                            </a>

                          )

                        }

                      </div>

                    </article>

                  );

                }

              )

            }

          </div>

        )

      }

    </aside>

  );

}