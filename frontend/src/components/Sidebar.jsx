import {

  BrainCircuit,
  MessageSquareText,
  FileText,
  Search,
  Sparkles,
  PanelLeft,
  Database,
  Clock3

} from "lucide-react";

export default function Sidebar() {

  return (

    <div className="modern-sidebar">

      {/* ============================= */}
      {/* LOGO */}
      {/* ============================= */}

      <div className="sidebar-top">

        <div className="sidebar-logo">

          <div className="logo-icon">

            <BrainCircuit size={22} />

          </div>

          <div>

            <h2>DELBot</h2>

            <span>
              Academic Intelligence
            </span>

          </div>

        </div>

      </div>

      {/* ============================= */}
      {/* NAVIGATION */}
      {/* ============================= */}

      <div className="sidebar-nav">

        <div className="nav-section-title">

          Workspace

        </div>

        <button className="sidebar-item active">

          <MessageSquareText size={18} />

          <span>Research Chat</span>

        </button>

        <button className="sidebar-item">

          <Search size={18} />

          <span>Semantic Search</span>

        </button>

        <button className="sidebar-item">

          <FileText size={18} />

          <span>Documents</span>

        </button>

        <button className="sidebar-item">

          <Database size={18} />

          <span>Knowledge Base</span>

        </button>

      </div>

      {/* ============================= */}
      {/* RECENT */}
      {/* ============================= */}

      <div className="sidebar-recent">

        <div className="nav-section-title">

          Recent Sessions

        </div>

        <div className="recent-card">

          <Clock3 size={14} />

          <div>

            <h4>
              NLP Healthcare
            </h4>

            <span>
              12 academic sources
            </span>

          </div>

        </div>

        <div className="recent-card">

          <Clock3 size={14} />

          <div>

            <h4>
              Transformer Research
            </h4>

            <span>
              Hybrid retrieval analysis
            </span>

          </div>

        </div>

      </div>

      {/* ============================= */}
      {/* FOOTER */}
      {/* ============================= */}

      <div className="sidebar-footer">

        <div className="ai-status">

          <Sparkles size={14} />

          DEL Intelligence Active

        </div>

      </div>

    </div>
  );
}