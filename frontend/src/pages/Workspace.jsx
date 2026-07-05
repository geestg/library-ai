import ResearchSession from "../components/workspace/ResearchSession";
import Sidebar from "../components/Sidebar";
import SearchPanel from "../components/SearchPanel";
import ThesisDrawer from "../components/sources/ThesisDrawer";

import useWorkspace from "../hooks/useWorkspace";

export default function Workspace() {

  const {

    // =====================================
    // SESSION
    // =====================================

    sessionId,

    // =====================================
    // CONVERSATION
    // =====================================

    messages,
    setMessages,

    // =====================================
    // SOURCES
    // =====================================

    sources,
    setSources,

    // =====================================
    // RESEARCH PROFILE
    // =====================================

    researchProfile,
    setResearchProfile,

    // =====================================
    // LEGACY
    // =====================================

    evidence,
    setEvidence,

    evidenceMatrix,
    setEvidenceMatrix,

    gapAnalysis,
    setGapAnalysis,

    // =====================================
    // UI
    // =====================================

    activeCitation,
    setActiveCitation,

    selectedThesis,
    setSelectedThesis,

  } = useWorkspace();

  return (

    <div className="workspace-shell">

      <div className="ambient-glow ambient-left" />

      <div className="ambient-glow ambient-right" />

      {/* ============================= */}
      {/* SIDEBAR */}
      {/* ============================= */}

      <aside className="workspace-sidebar">

        <Sidebar />

      </aside>

      {/* ============================= */}
      {/* RESEARCH SESSION */}
      {/* ============================= */}

      <main className="workspace-main">

        <ResearchSession

          // =================================
          // SESSION
          // =================================

          sessionId={sessionId}

          // =================================
          // CONVERSATION
          // =================================

          messages={messages}
          setMessages={setMessages}

          // =================================
          // SOURCES
          // =================================

          sources={sources}
          setSources={setSources}

          // =================================
          // EVIDENCE
          // =================================

          evidence={evidence}
          setEvidence={setEvidence}

          evidenceMatrix={evidenceMatrix}
          setEvidenceMatrix={setEvidenceMatrix}

          gapAnalysis={gapAnalysis}
          setGapAnalysis={setGapAnalysis}

          // =================================
          // RESEARCH PROFILE
          // =================================

          researchProfile={researchProfile}
          setResearchProfile={setResearchProfile}

          // =================================
          // UI
          // =================================

          activeCitation={activeCitation}
          setActiveCitation={setActiveCitation}

          setSelectedThesis={setSelectedThesis}

        />

      </main>

      {/* ============================= */}
      {/* RESEARCH PANEL */}
      {/* ============================= */}

      <aside className="workspace-evidence">

        <SearchPanel

          sources={sources}

          researchProfile={researchProfile}

          activeCitation={activeCitation}

          setActiveCitation={setActiveCitation}

          setSelectedThesis={setSelectedThesis}

        />

      </aside>

      {/* ============================= */}
      {/* THESIS DRAWER */}
      {/* ============================= */}

      <ThesisDrawer

        thesis={selectedThesis}

        onClose={() =>

          setSelectedThesis(null)

        }

      />

    </div>

  );

}