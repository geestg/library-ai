export default function NoveltyCard({

  noveltyAnalysis

}) {

  if (!noveltyAnalysis) {

    return null;

  }

  const noveltyScore =

    noveltyAnalysis
      ?.novelty_score ?? 0;

  const noveltyLevel =

    noveltyAnalysis
      ?.novelty_level || "LOW";

  const reasons =

    noveltyAnalysis
      ?.reasons || [];

  return (

    <div
      className="
      novelty-card
      "
    >

      {/* ======================== */}
      {/* HEADER */}
      {/* ======================== */}

      <div
        className="
        novelty-header
        "
      >

        <span>

          Novelty Score

        </span>

        <strong>

          {noveltyScore} / 10

        </strong>

      </div>

      {/* ======================== */}
      {/* PROGRESS BAR */}
      {/* ======================== */}

      <div
        className="
        novelty-progress
        "
      >

        <div

          className="
          novelty-progress-fill
          "

          style={{

            width:
              `${noveltyScore * 10}%`

          }}

        />

      </div>

      {/* ======================== */}
      {/* LEVEL */}
      {/* ======================== */}

      <div

        className={`novelty-level ${
          noveltyLevel.toLowerCase()
        }`}

      >

        {noveltyLevel}

      </div>

      {/* ======================== */}
      {/* REASONS */}
      {/* ======================== */}

      {

        reasons.length > 0 && (

          <ul
            className="
            novelty-reasons
            "
          >

            {

              reasons.map(

                (
                  reason,
                  idx
                ) => (

                  <li
                    key={idx}
                  >

                    {reason}

                  </li>

                )

              )

            }

          </ul>

        )

      }

    </div>

  );

}