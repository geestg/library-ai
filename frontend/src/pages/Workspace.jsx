import { useState } from "react";

import Sidebar from "../components/Sidebar";

import ChatWindow from "../components/chat/ChatWindow";

import SearchPanel from "../components/SearchPanel";

import ThesisDrawer from "../components/sources/ThesisDrawer";

export default function Workspace() {

  // =====================================
  // CHAT STATE
  // =====================================

  const [messages, setMessages] =
    useState([]);

  // =====================================
  // CITATION SOURCES
  // =====================================

  const [sources, setSources] =
    useState([]);

  // =====================================
  // STRUCTURED EVIDENCE
  // =====================================

  const [evidence, setEvidence] =
    useState({});

  // =====================================
  // EVIDENCE MATRIX
  // =====================================

  const [

    evidenceMatrix,

    setEvidenceMatrix

  ] = useState({});

  // =====================================
  // GAP ANALYSIS
  // =====================================

  const [

    gapAnalysis,

    setGapAnalysis

  ] = useState({});

  // =====================================
  // ACTIVE CITATION
  // =====================================

  const [

    activeCitation,

    setActiveCitation

  ] = useState(null);

  // =====================================
  // SELECTED THESIS
  // =====================================

  const [

    selectedThesis,

    setSelectedThesis

  ] = useState(null);

  // =====================================
  // ACTIVE DOCUMENT
  // =====================================

  const [

    activeDocument,

    setActiveDocument

  ] = useState(null);

  return (

    <div className="workspace-shell">

      {/* ========================= */}
      {/* AMBIENT GLOW */}
      {/* ========================= */}

      <div className="ambient-glow ambient-left" />

      <div className="ambient-glow ambient-right" />

      {/* ========================= */}
      {/* SIDEBAR */}
      {/* ========================= */}

      <aside className="workspace-sidebar">

        <Sidebar />

      </aside>

      {/* ========================= */}
      {/* MAIN CHAT */}
      {/* ========================= */}

      <main className="workspace-main">

        <ChatWindow

          messages={messages}

          setMessages={setMessages}

          sources={sources}

          setSources={setSources}

          setEvidence={setEvidence}

          setEvidenceMatrix={setEvidenceMatrix}

          setGapAnalysis={setGapAnalysis}

          activeCitation={activeCitation}

          setActiveCitation={setActiveCitation}

          setSelectedThesis={
            setSelectedThesis
          }

        />

      </main>

      {/* ========================= */}
      {/* EVIDENCE PANEL */}
      {/* ========================= */}

      <aside className="workspace-evidence">

        <SearchPanel

          sources={sources}

          activeCitation={activeCitation}

          setActiveCitation={
            setActiveCitation
          }

          setSelectedThesis={
            setSelectedThesis
          }

        />
        
      </aside>

      {/* ========================= */}
      {/* THESIS DRAWER */}
      {/* ========================= */}

      <ThesisDrawer

        thesis={
          selectedThesis
        }

        onClose={() =>

          setSelectedThesis(
            null
          )

        }

      />

    </div>

  );

}