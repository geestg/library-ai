import {
  GraduationCap,
  Target,
  CheckCircle2,
  BookOpen
} from "lucide-react";

export default function ProdiWidget({

  prodi

}) {

  if (!prodi) {

    return null;

  }

  const {

    prodi: programName = "General",

    research_alignment = 0,

    focus_areas = [],

    matched_competencies = []

  } = prodi;

  const alignment = Math.round(
    research_alignment * 100
  );

  return (

    <div className="research-widget">

      {/* ========================= */}
      {/* HEADER */}
      {/* ========================= */}

      <div className="research-widget-header">

        <div className="research-widget-title">

          <GraduationCap size={16} />

          Academic Alignment

        </div>

      </div>

      {/* ========================= */}
      {/* PROGRAM */}
      {/* ========================= */}

      <div className="prodi-summary">

        <div className="prodi-name">

          {programName}

        </div>

        <div className="prodi-alignment">

          {alignment}%

        </div>

      </div>

      {/* ========================= */}
      {/* PROGRESS */}
      {/* ========================= */}

      <div className="novelty-progress">

        <div

          className="novelty-progress-fill"

          style={{

            width: `${alignment}%`

          }}

        />

      </div>

      {/* ========================= */}
      {/* FOCUS AREA */}
      {/* ========================= */}

      {

        focus_areas.length > 0 && (

          <>

            <div className="widget-subtitle">

              <Target size={14} />

              Research Focus

            </div>

            <div className="trend-tags">

              {

                focus_areas.map(

                  (area, index) => (

                    <div

                      key={index}

                      className="trend-tag"

                    >

                      {area}

                    </div>

                  )

                )

              }

            </div>

          </>

        )

      }

      {/* ========================= */}
      {/* MATCHED */}
      {/* ========================= */}

      {

        matched_competencies.length > 0 && (

          <>

            <div className="widget-subtitle">

              <BookOpen size={14} />

              Matched Competencies

            </div>

            <div className="gap-list">

              {

                matched_competencies.map(

                  (

                    competency,

                    index

                  ) => (

                    <div

                      key={index}

                      className="gap-item"

                    >

                      <CheckCircle2

                        size={14}

                      />

                      <span>

                        {competency}

                      </span>

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