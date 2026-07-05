import {
  Search,
  FlaskConical,
  Database,
  Clock3,
  CheckCircle2
} from "lucide-react";

export default function GapWidget({

  gap

}) {

  if (!gap) {

    return null;

  }

  const methodGap =

    gap.method_gap || [];

  const datasetGap =

    gap.dataset_gap || [];

  const temporalGap =

    gap.temporal_gap || [];

  const evaluationGap =

    gap.evaluation_gap || [];

  const renderSection = (

    title,

    icon,

    items

  ) => {

    if (!items.length) {

      return null;

    }

    return (

      <div className="gap-section">

        <div className="gap-title">

          {icon}

          <span>

            {title}

          </span>

        </div>

        <div className="gap-list">

          {

            items.map(

              (item, index) => (

                <div

                  key={index}

                  className="gap-item"

                >

                  <CheckCircle2

                    size={14}

                  />

                  <span>

                    {

                      typeof item === "string"

                        ? item

                        : JSON.stringify(item)

                    }

                  </span>

                </div>

              )

            )

          }

        </div>

      </div>

    );

  };

  return (

    <div className="research-widget">

      {/* ========================= */}
      {/* HEADER */}
      {/* ========================= */}

      <div className="research-widget-header">

        <div className="research-widget-title">

          <Search size={16} />

          Research Gap

        </div>

      </div>

      {

        renderSection(

          "Method Gap",

          <FlaskConical size={14} />,

          methodGap

        )

      }

      {

        renderSection(

          "Dataset Gap",

          <Database size={14} />,

          datasetGap

        )

      }

      {

        renderSection(

          "Temporal Gap",

          <Clock3 size={14} />,

          temporalGap

        )

      }

      {

        renderSection(

          "Evaluation Gap",

          <CheckCircle2 size={14} />,

          evaluationGap

        )

      }

      {

        !methodGap.length &&
        !datasetGap.length &&
        !temporalGap.length &&
        !evaluationGap.length && (

          <div className="research-empty">

            No significant research gap detected.

          </div>

        )

      }

    </div>

  );

}