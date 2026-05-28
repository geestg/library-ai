import { useState } from "react";

import Sidebar from "../components/Sidebar";

import ChatWindow from "../components/chat/ChatWindow";

import SearchPanel from "../components/SearchPanel";


export default function Workspace() {

  // =====================================
  // STATE
  // =====================================

  const [messages, setMessages] =
    useState([]);

  const [sources, setSources] =
    useState([]);

  const [activeCitation, setActiveCitation] =
    useState(null);

  // =====================================
  // UI
  // =====================================

  return (

    <div className="workspace-shell">

      {/* ============================= */}
      {/* AMBIENT GLOW */}
      {/* ============================= */}

      <div className="ambient-glow ambient-left" />
      <div className="ambient-glow ambient-right" />

      {/* ============================= */}
      {/* SIDEBAR */}
      {/* ============================= */}

      <aside className="workspace-sidebar">

        <Sidebar />

      </aside>

      {/* ============================= */}
      {/* MAIN */}
      {/* ============================= */}

      <main className="workspace-main">

        <ChatWindow

          messages={messages}

          setMessages={setMessages}

          setSources={setSources}

          activeCitation={activeCitation}

          setActiveCitation={
            setActiveCitation
          }

        />

      </main>

      {/* ============================= */}
      {/* EVIDENCE */}
      {/* ============================= */}

      <aside className="workspace-evidence">

        <SearchPanel

          sources={sources}

          activeCitation={
            activeCitation
          }

        />

      </aside>

    </div>
  );
}