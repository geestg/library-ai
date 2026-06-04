import {
  X,
  FileText,
  User,
  Calendar,
  GraduationCap,
  ExternalLink,
  BarChart3
} from "lucide-react";

export default function ThesisDrawer({

  thesis,

  onClose

}) {

  if (!thesis) {
    return null;
  }

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

        {/* ================================= */}
        {/* HEADER */}
        {/* ================================= */}

        <div className="thesis-drawer-header">

          <div>

            <div className="drawer-badge">

              Thesis Details

            </div>

            <h2>

              {thesis.title ||
                "Unknown Thesis"}

            </h2>

          </div>

          <button

            className="drawer-close"

            onClick={onClose}

          >

            <X size={18} />

          </button>

        </div>

        {/* ================================= */}
        {/* META */}
        {/* ================================= */}

        <div className="thesis-meta-grid">

          <div className="thesis-meta-card">

            <User size={16} />

            <div>

              <span>Author</span>

              <strong>

                {thesis.author ||
                  "-"}

              </strong>

            </div>

          </div>

          <div className="thesis-meta-card">

            <Calendar size={16} />

            <div>

              <span>Year</span>

              <strong>

                {thesis.year ||
                  "-"}

              </strong>

            </div>

          </div>

          <div className="thesis-meta-card">

            <GraduationCap
              size={16}
            />

            <div>

              <span>Program</span>

              <strong>

                {thesis.prodi ||
                  "-"}

              </strong>

            </div>

          </div>

          <div className="thesis-meta-card">

            <BarChart3
              size={16}
            />

            <div>

              <span>Score</span>

              <strong>

                {Number(
                  thesis.score || 0
                ).toFixed(2)}

              </strong>

            </div>

          </div>

        </div>

        {/* ================================= */}
        {/* ABSTRACT */}
        {/* ================================= */}

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

        {/* ================================= */}
        {/* RETRIEVED EVIDENCE */}
        {/* ================================= */}

        <div className="thesis-section">

          <div className="section-title">

            <FileText size={16} />

            Retrieved Evidence

          </div>

          <div className="evidence-content">

            {

              thesis.chunk ||

              "No retrieved evidence available."

            }

          </div>

        </div>

        {/* ================================= */}
        {/* REPOSITORY */}
        {/* ================================= */}

        {

          thesis.url && (

            <div className="thesis-section">

              <div className="section-title">

                <ExternalLink
                  size={16}
                />

                Repository

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