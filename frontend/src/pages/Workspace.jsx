import {
  useState,
  useEffect
} from "react";

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

  // =====================================
  // LOAD STORAGE
  // =====================================

  useEffect(() => {

    try {

      const rawData =
        localStorage.getItem(
          "delbot_workspace"
        );

      if (!rawData) {
        return;
      }

      const savedData =
        JSON.parse(rawData);

      if (
        Array.isArray(
          savedData.messages
        )
      ) {

        setMessages(
          savedData.messages
        );

      }

      if (
        Array.isArray(
          savedData.sources
        )
      ) {

        setSources(
          savedData.sources
        );

      }

      if (
        savedData.evidence
      ) {

        setEvidence(
          savedData.evidence
        );

      }

      if (
        savedData.evidenceMatrix
      ) {

        setEvidenceMatrix(
          savedData.evidenceMatrix
        );

      }

      if (
        savedData.gapAnalysis
      ) {

        setGapAnalysis(
          savedData.gapAnalysis
        );

      }

      console.log(
        "[DELBOT] Workspace restored"
      );

    } catch (err) {

      console.error(
        "[DELBOT] Failed loading workspace",
        err
      );

      localStorage.removeItem(
        "delbot_workspace"
      );

    }

  }, []);

  // =====================================
  // SAVE STORAGE
  // =====================================

  useEffect(() => {

    try {

      localStorage.setItem(

        "delbot_workspace",

        JSON.stringify({

          messages,

          sources,

          evidence,

          evidenceMatrix,

          gapAnalysis

        })

      );

    } catch (err) {

      console.error(
        "[DELBOT] Failed saving workspace",
        err
      );

    }

  }, [

    messages,

    sources,

    evidence,

    evidenceMatrix,

    gapAnalysis

  ]);

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
      {/* SOURCE PANEL */}
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