import { useState } from "react";

import Sidebar from "../components/Sidebar";

import ChatWindow from "../components/chat/ChatWindow";

import SearchPanel from "../components/SearchPanel";

export default function Workspace() {

  const [messages, setMessages] =
    useState([]);

  const [sources, setSources] =
    useState([]);

  const [activeCitation, setActiveCitation] =
    useState(null);

  return (

    <div className="workspace-shell">

      <div className="ambient-glow ambient-left" />

      <div className="ambient-glow ambient-right" />

      <aside className="workspace-sidebar">

        <Sidebar />

      </aside>

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