import {
  TrendingUp,
  Cpu,
  FlaskConical,
  Database,
  Sparkles
} from "lucide-react";

export default function TrendWidget({

  trend

}) {

  if (!trend) {

    return null;

  }

  const technologies =
    trend.top_technologies || [];

  const methods =
    trend.top_methods || [];

  const datasets =
    trend.top_datasets || [];

  const emerging =
    trend.emerging_topics || [];

  const firstTechnology =
    technologies[0];

  const firstMethod =
    methods[0];

  const firstDataset =
    datasets[0];

  return (

    <div className="research-widget">

      {/* ======================== */}
      {/* HEADER */}
      {/* ======================== */}

      <div className="research-widget-header">

        <div className="research-widget-title">

          <TrendingUp size={16} />

          Research Trends

        </div>

      </div>

      {/* ======================== */}
      {/* DOMINANT TECHNOLOGY */}
      {/* ======================== */}

      {

        firstTechnology && (

          <div className="trend-item">

            <Cpu size={15} />

            <div>

              <span>

                Dominant Technology

              </span>

              <strong>

                {firstTechnology[0]}

              </strong>

            </div>

          </div>

        )

      }

      {/* ======================== */}
      {/* DOMINANT METHOD */}
      {/* ======================== */}

      {

        firstMethod && (

          <div className="trend-item">

            <FlaskConical size={15} />

            <div>

              <span>

                Dominant Method

              </span>

              <strong>

                {firstMethod[0]}

              </strong>

            </div>

          </div>

        )

      }

      {/* ======================== */}
      {/* DOMINANT DATASET */}
      {/* ======================== */}

      {

        firstDataset && (

          <div className="trend-item">

            <Database size={15} />

            <div>

              <span>

                Dominant Dataset

              </span>

              <strong>

                {firstDataset[0]}

              </strong>

            </div>

          </div>

        )

      }

      {/* ======================== */}
      {/* EMERGING */}
      {/* ======================== */}

      {

        emerging.length > 0 && (

          <>

            <div className="trend-divider" />

            <div className="trend-subtitle">

              <Sparkles size={14} />

              Emerging Topics

            </div>

            <div className="trend-tags">

              {

                emerging.map(

                  (item, index) => (

                    <div

                      key={index}

                      className="trend-tag"

                    >

                      {item}

                    </div>

                  )

                )

              }

            </div>

          </>

        )

      }

    </div>

  );

}