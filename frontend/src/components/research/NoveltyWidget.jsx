import {
  Sparkles,
  TrendingUp
} from "lucide-react";

export default function NoveltyWidget({

  novelty

}) {

  if (!novelty) {

    return null;

  }

  const score =

    novelty.novelty_score ?? 0;

  const level =

    novelty.novelty_level ||

    "LOW";

  const reasons =

    novelty.reasons || [];

  const percentage =

    Math.min(

      score * 10,

      100

    );

  return (

    <div className="research-widget">

      {/* ========================= */}
      {/* HEADER */}
      {/* ========================= */}

      <div className="research-widget-header">

        <div className="research-widget-title">

          <Sparkles size={16} />

          Novelty Assessment

        </div>

        <div className={`novelty-badge ${level.toLowerCase()}`}>

          {level}

        </div>

      </div>

      {/* ========================= */}
      {/* SCORE */}
      {/* ========================= */}

      <div className="novelty-score-wrapper">

        <div className="novelty-score">

          {score}

          <span>

            /10

          </span>

        </div>

      </div>

      {/* ========================= */}
      {/* BAR */}
      {/* ========================= */}

      <div className="novelty-progress">

        <div

          className="novelty-progress-fill"

          style={{

            width: `${percentage}%`

          }}

        />

      </div>

      {/* ========================= */}
      {/* REASONS */}
      {/* ========================= */}

      {

        reasons.length > 0 && (

          <div className="research-widget-body">

            {

              reasons.map(

                (reason, index) => (

                  <div

                    key={index}

                    className="research-reason"

                  >

                    <TrendingUp

                      size={14}

                    />

                    <span>

                      {reason}

                    </span>

                  </div>

                )

              )

            }

          </div>

        )

      }

    </div>

  );

}