import {
  X,
  FileText,
  User,
  Calendar,
  GraduationCap,
  ExternalLink,
  BarChart3,
  Cpu,
  Database,
  FlaskConical,
  CheckCircle2
} from "lucide-react";

export default function ThesisDrawer({

  thesis,

  onClose

}) {

  if (!thesis) {
    return null;
  }

  const renderTags = (
    items,
    emptyText
  ) => {

    if (
      !items ||
      items.length === 0
    ) {

      return (

        <div className="empty-evidence">

          {emptyText}

        </div>

      );
    }

    return (

      <div className="evidence-tags">

        {

          items.map(

            (
              item,
              idx
            ) => (

              <div
                key={idx}
                className="evidence-tag"
              >

                {item}

              </div>

            )

          )

        }

      </div>

    );
  };

  return (

    <div
      className="thesis-drawer-overlay"
      onClick={onClose}
    >

      <div

        className="thesis-drawer"

        onClick={(e) =>
          e.stopPropagation()
        }

      >

        {/* HEADER */}

        <div className="thesis-drawer-header">

          <div>

            <div className="drawer-badge">

              Thesis Details

            </div>

            <h2>

              {
                thesis.title ||
                "Unknown Thesis"
              }

            </h2>

          </div>

          <button

            className="drawer-close"

            onClick={onClose}

          >

            <X size={18} />

          </button>

        </div>

        {/* META */}

        <div className="thesis-meta-grid">

          <div className="thesis-meta-card">

            <User size={16} />

            <div>

              <span>
                Author
              </span>

              <strong>

                {
                  thesis.author ||
                  "-"
                }

              </strong>

            </div>

          </div>

          <div className="thesis-meta-card">

            <Calendar size={16} />

            <div>

              <span>
                Year
              </span>

              <strong>

                {
                  thesis.year ||
                  "-"
                }

              </strong>

            </div>

          </div>

          <div className="thesis-meta-card">

            <GraduationCap size={16} />

            <div>

              <span>
                Program
              </span>

              <strong>

                {
                  thesis.prodi ||
                  "-"
                }

              </strong>

            </div>

          </div>

          <div className="thesis-meta-card">

            <BarChart3 size={16} />

            <div>

              <span>
                Relevance
              </span>

              <strong>

                {
                  Number(
                    thesis.score || 0
                  ).toFixed(2)
                }

              </strong>

            </div>

          </div>

        </div>

        {/* ABSTRACT */}

        <div className="thesis-section">

          <div className="section-title">

            <FileText size={16} />

            Abstract

          </div>

          <div className="section-content">

            {

              thesis.abstract ||

              "Abstract not available."

            }

          </div>

        </div>

        {/* RETRIEVED EVIDENCE */}

        <div className="thesis-section">

          <div className="section-title">

            <Cpu size={16} />

            Retrieved Evidence

          </div>

          <div className="evidence-grid">

            <div className="evidence-box">

              <div className="evidence-title">

                <Cpu size={14} />

                Technology

              </div>

              {

                renderTags(

                  thesis.technologies,

                  "No technology detected"

                )

              }

            </div>

            <div className="evidence-box">

              <div className="evidence-title">

                <FlaskConical size={14} />

                Methodology

              </div>

              {

                renderTags(

                  thesis.methodologies,

                  "No methodology detected"

                )

              }

            </div>

            <div className="evidence-box">

              <div className="evidence-title">

                <Database size={14} />

                Dataset

              </div>

              {

                renderTags(

                  thesis.datasets,

                  "No dataset detected"

                )

              }

            </div>

            <div className="evidence-box">

              <div className="evidence-title">

                <CheckCircle2 size={14} />

                Evaluation

              </div>

              {

                renderTags(

                  thesis.evaluation_metrics,

                  "No evaluation metric detected"

                )

              }

            </div>

          </div>

        </div>

        {/* REPOSITORY */}

        {

          thesis.url && (

            <div className="thesis-section">

              <div className="section-title">

                

                

              </div>

              <a

                href={thesis.url}

                target="_blank"

                rel="noopener noreferrer"

                className="repository-btn"

              >

                <ExternalLink
                  size={15}
                />

                Open Repository

              </a>

            </div>

          )

        }

      </div>

    </div>

  );

}