import {
  BrainCircuit,
  Cpu,
  Layers3
} from "lucide-react";

export default function CompetencyWidget({

  competency

}) {

  if (!competency) {

    return null;

  }

  const competencies =

    competency.competencies || [];

  return (

    <div className="research-widget">

      {/* ========================= */}
      {/* HEADER */}
      {/* ========================= */}

      <div className="research-widget-header">

        <div className="research-widget-title">

          <BrainCircuit size={16} />

          Required Competencies

        </div>

      </div>

      {

        competencies.length === 0 && (

          <div className="research-empty">

            Competency information is not available.

          </div>

        )

      }

      {

        competencies.map(

          (

            item,

            index

          ) => (

            <div

              key={index}

              className="competency-item"

            >

              <div className="competency-icon">

                <Cpu size={14} />

              </div>

              <div className="competency-content">

                <div className="competency-name">

                  {

                    item.name

                  }

                </div>

                <div className="competency-count">

                  Mentioned in

                  {" "}

                  <strong>

                    {

                      item.count

                    }

                  </strong>

                  {" "}

                  retrieved thesis

                </div>

              </div>

              <div className="competency-rank">

                <Layers3 size={15} />

              </div>

            </div>

          )

        )

      }

    </div>

  );

}