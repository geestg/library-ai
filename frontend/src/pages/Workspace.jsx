import { useState, useEffect, useCallback } from "react";
import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/chat/ChatWindow";
import SearchPanel from "../components/SearchPanel";
import ThesisDrawer from "../components/sources/ThesisDrawer";
import IntroSplash from "../components/IntroSplash";
import LandingSelection from "../components/auth/LandingSelection";
import { createSession, getSession, getSessionHistory, deleteSession } from "../services/sessionApi";

export default function Workspace() {
  const [showSplash, setShowSplash] = useState(true);
  // =====================================
  // DYNAMIC SESSION & WORKSPACE STATE
  // =====================================
  const [sessionId, setSessionId] = useState(() => `session_${Date.now()}`);
  const [historySessions, setHistorySessions] = useState([]);
  const [messages, setMessages] = useState([]);
  const [sources, setSources] = useState([]);
  const [evidence, setEvidence] = useState({});
  const [activeCitation, setActiveCitation] = useState(null);
  const [selectedThesis, setSelectedThesis] = useState(null);
  const [activeDocument, setActiveDocument] = useState(null);

  const [isLoggedIn, setIsLoggedIn] = useState(
    () => localStorage.getItem("isLoggedIn") === "true"
  );
  const [userRole, setUserRole] = useState(
    () => localStorage.getItem("userRole") || "student"
  );
  const [userInfo, setUserInfo] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem("userInfo")) || null;
    } catch {
      return null;
    }
  });

  const handleRoleChange = (role) => {
    setUserRole(role);
    localStorage.setItem("userRole", role);
  };

  const handleGuestLogin = () => {
    setUserRole("guest");
    localStorage.setItem("userRole", "guest");
    setIsLoggedIn(true);
    localStorage.setItem("isLoggedIn", "true");
    const info = { name: "Tamu Umum", id: "GUEST", prodi: "Umum" };
    setUserInfo(info);
    localStorage.setItem("userInfo", JSON.stringify(info));
  };

  const handleLoginSuccess = (role, info) => {
    setUserRole(role);
    localStorage.setItem("userRole", role);
    setIsLoggedIn(true);
    localStorage.setItem("isLoggedIn", "true");
    setUserInfo(info);
    localStorage.setItem("userInfo", JSON.stringify(info));
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    localStorage.removeItem("isLoggedIn");
    setUserRole("student");
    localStorage.setItem("userRole", "student");
    setUserInfo(null);
    localStorage.removeItem("userInfo");
  };

  // =====================================
  // FETCH SESSION HISTORY LIST
  // =====================================
  const fetchHistory = useCallback(async () => {
    const history = await getSessionHistory();
    if (Array.isArray(history)) {
      setHistorySessions(history);
    }
  }, []);

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  // =====================================
  // NEW CHAT ACTION
  // =====================================
  const handleNewChat = async () => {
    try {
      const newSession = await createSession();
      const newId = newSession?.session_id || `session_${Date.now()}`;
      setSessionId(newId);
      setMessages([]);
      setSources([]);
      setEvidence({});
      setActiveCitation(null);
      setSelectedThesis(null);
      setActiveDocument(null);
      await fetchHistory();
    } catch (err) {
      console.error("[handleNewChat Error]", err);
      setSessionId(`session_${Date.now()}`);
      setMessages([]);
      setSources([]);
      setEvidence({});
    }
  };

  // =====================================
  // SELECT SESSION FROM HISTORY
  // =====================================
  const handleSelectSession = async (targetSessionId) => {
    if (targetSessionId === sessionId) return;

    try {
      setSessionId(targetSessionId);
      const sessionData = await getSession(targetSessionId);

      if (sessionData && sessionData.conversation) {
        const rawMessages = sessionData.conversation.messages || [];
        const formattedMessages = rawMessages.map((msg, idx) => ({
          id: `${Date.now()}-${idx}`,
          role: msg.role,
          content: msg.content,
          citations: msg.citations || [],
          sources: msg.sources || [],
        }));

        // Extract sources from execution session, session state, or from assistant messages
        const execCtx = sessionData.execution?.serialized_context;
        let extractedSources =
          sessionData.sources ||
          sessionData.citations ||
          execCtx?.citations ||
          execCtx?.sources ||
          [];

        if (!extractedSources || extractedSources.length === 0) {
          for (const m of [...formattedMessages].reverse()) {
            if (m.role === "assistant" && (m.sources?.length > 0 || m.citations?.length > 0)) {
              extractedSources = m.sources?.length > 0 ? m.sources : m.citations;
              break;
            }
          }
        }

        setMessages(formattedMessages);
        setSources(extractedSources || []);
      } else {
        setMessages([]);
        setSources([]);
      }
    } catch (err) {
      console.error("[handleSelectSession Error]", err);
    }
  };

  // =====================================
  // DELETE SESSION
  // =====================================
  const handleDeleteSession = async (targetSessionId) => {
    try {
      await deleteSession(targetSessionId);
      if (targetSessionId === sessionId) {
        handleNewChat();
      } else {
        fetchHistory();
      }
    } catch (err) {
      console.error("[handleDeleteSession Error]", err);
    }
  };

  if (showSplash) {
    return <IntroSplash onFinish={() => setShowSplash(false)} />;
  }

  if (!isLoggedIn) {
    return <LandingSelection onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div className={`workspace-shell ${sources.length === 0 || userRole === "guest" ? "hide-evidence" : ""}`}>
      {/* ========================= */}
      {/* AMBIENT GLOW */}
      {/* ========================= */}
      <div className="ambient-glow ambient-left" />
      <div className="ambient-glow ambient-right" />

      {/* ========================= */}
      {/* SIDEBAR */}
      {/* ========================= */}
      <aside className="workspace-sidebar">
        <Sidebar
          userRole={userRole}
          setUserRole={handleRoleChange}
          userInfo={userInfo}
          onLogout={handleLogout}
          historySessions={historySessions}
          activeSessionId={sessionId}
          onNewChat={handleNewChat}
          onSelectSession={handleSelectSession}
          onDeleteSession={handleDeleteSession}
        />
      </aside>

      {/* ========================= */}
      {/* MAIN CHAT */}
      {/* ========================= */}
      <main className="workspace-main">
        <ChatWindow
          userRole={userRole}
          sessionId={sessionId}
          messages={messages}
          setMessages={setMessages}
          setSources={setSources}
          setEvidence={setEvidence}
          activeCitation={activeCitation}
          setActiveCitation={setActiveCitation}
          selectedThesis={selectedThesis}
          setSelectedThesis={setSelectedThesis}
          activeDocument={activeDocument}
          setActiveDocument={setActiveDocument}
          onMessageSent={fetchHistory}
        />
      </main>

      {/* ========================= */}
      {/* EVIDENCE PANEL */}
      {/* ========================= */}
      {userRole !== "guest" && (
        <aside className="workspace-evidence">
          <SearchPanel
            sources={sources}
            evidence={evidence}
            activeCitation={activeCitation}
            setActiveCitation={setActiveCitation}
            selectedThesis={selectedThesis}
            setSelectedThesis={setSelectedThesis}
          />
        </aside>
      )}

      {/* ========================= */}
      {/* THESIS DRAWER */}
      {/* ========================= */}
      {selectedThesis && (
        <ThesisDrawer
          thesis={selectedThesis}
          onClose={() => setSelectedThesis(null)}
        />
      )}
    </div>
  );
}