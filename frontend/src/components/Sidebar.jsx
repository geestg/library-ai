import { useState } from "react";
import { createPortal } from "react-dom";
import { BrainCircuit, Plus, MessageSquare, ChevronDown, Lock, X, Trash2 } from "lucide-react";

export default function Sidebar({
  userRole,
  setUserRole,
  userInfo,
  onLogout,
  historySessions = [],
  activeSessionId,
  onNewChat,
  onSelectSession,
  onDeleteSession,
}) {
  const [showProfileModal, setShowProfileModal] = useState(false);

  const handleUserCardClick = () => {
    setShowProfileModal(true);
  };

  return (
    <>
      <aside className="modern-sidebar">
        {/* ============================= */}
        {/* BRAND & ACTION */}
        {/* ============================= */}
        <div className="sidebar-top">
          <div className="sidebar-logo">
            <div className="logo-icon">
              <BrainCircuit size={20} />
            </div>
            <div className="logo-meta">
              <h2>DELBot</h2>
              <span className="logo-subtitle">IT Del Library Agent</span>
            </div>
          </div>

          {/* ============================= */}
          {/* NEW CHAT BUTTON */}
          {/* ============================= */}
          <button className="new-chat-btn" onClick={onNewChat} type="button">
            <Plus size={16} color="#0f172a" />
            <span>Percakapan Baru</span>
          </button>
        </div>

        {/* ============================= */}
        {/* DYNAMIC HISTORY CONTAINER */}
        {/* ============================= */}
        <div className="sidebar-history">
          <span className="history-label">RIWAYAT PERCAKAPAN</span>
          <div className="history-list">
            {historySessions.length === 0 ? (
              <div style={{ padding: "12px 8px", fontSize: "0.78rem", color: "#94a3b8", fontStyle: "italic" }}>
                Belum ada riwayat percakapan. Mulai obrolan baru!
              </div>
            ) : (
              historySessions.map((session) => {
                const isActive = session.session_id === activeSessionId;
                return (
                  <div
                    key={session.session_id}
                    className={`history-item ${isActive ? "active" : ""}`}
                    onClick={() => onSelectSession?.(session.session_id)}
                  >
                    <div className="history-item-text">
                      <MessageSquare size={14} className="history-icon" color={isActive ? "#0f172a" : "#64748b"} />
                      <span className="history-title">
                        {session.title || "Percakapan Riset"}
                      </span>
                    </div>

                    {onDeleteSession && (
                      <button
                        type="button"
                        className="history-delete-btn"
                        onClick={(e) => {
                          e.stopPropagation();
                          onDeleteSession(session.session_id);
                        }}
                        title="Hapus Percakapan"
                      >
                        <Trash2 size={13} />
                      </button>
                    )}
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* ============================= */}
        {/* USER CARD (TOGGLE ON CLICK) */}
        {/* ============================= */}
        <div
          className="sidebar-user-card"
          onClick={handleUserCardClick}
          title="Klik untuk melihat profil atau ganti akun"
          style={{ display: "flex", alignItems: "center", gap: "10px", cursor: "pointer" }}
        >
          <div className="user-avatar" style={{ background: userRole === "admin" ? "linear-gradient(135deg, #4f46e5, #7c3aed)" : "linear-gradient(135deg, #0284c7, #38bdf8)" }}>
            <span>{userRole === "student" ? "M" : "P"}</span>
          </div>
          <div className="user-info" style={{ flex: 1 }}>
            <strong>{userInfo?.name || (userRole === "student" ? "Budi Pratama" : "Ibu Sari")}</strong>
            <span style={{ color: userRole === "admin" ? "#c084fc" : "#38bdf8", fontWeight: 600 }}>
              {userRole === "student" ? "Mahasiswa IT Del" : "Pengelola Perpus"}
            </span>
          </div>
            
            {/* LOGOUT BUTTON */}
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                onLogout();
              }}
              style={{
                background: "none",
                border: "none",
                cursor: "pointer",
                color: "#94a3b8",
                padding: "6px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                borderRadius: "50%",
                transition: "background 0.2s"
              }}
              title="Keluar / Logout"
              className="sidebar-logout-btn"
            >
              <X size={14} />
            </button>

            <div className="user-chevron">
              {userRole === "student" ? <Lock size={14} color="#94a3b8" /> : <ChevronDown size={14} />}
            </div>
          </div>
      </aside>

      {/* ============================= */}
      {/* USER PROFILE DETAIL MODAL */}
      {/* ============================= */}
      {showProfileModal &&
        createPortal(
          <div
            style={{
              position: "fixed",
              top: 0,
              left: 0,
              width: "100vw",
              height: "100vh",
              backgroundColor: "rgba(15, 23, 42, 0.75)",
              backdropFilter: "blur(8px)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              zIndex: 999999,
              padding: "20px",
              boxSizing: "border-box"
            }}
            onClick={() => setShowProfileModal(false)}
          >
            <div
              style={{
                background: "#ffffff",
                borderRadius: "20px",
                padding: "28px",
                width: "100%",
                maxWidth: "380px",
                boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.35)",
                border: "1px solid #e2e8f0",
                color: "#0f172a"
              }}
              onClick={(e) => e.stopPropagation()}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
                <h3 style={{ margin: 0, fontSize: "1.1rem", fontWeight: 800, color: "#0f172a" }}>
                  Profil Pengguna
                </h3>
                <button
                  type="button"
                  onClick={() => setShowProfileModal(false)}
                  style={{ background: "none", border: "none", cursor: "pointer", color: "#64748b" }}
                >
                  <X size={18} />
                </button>
              </div>

              {/* USER META DISPLAY */}
              <div style={{ display: "flex", alignItems: "center", gap: "14px", marginBottom: "20px", padding: "12px", background: "#f8fafc", borderRadius: "12px", border: "1px solid #e2e8f0" }}>
                <div style={{ width: "48px", height: "48px", borderRadius: "50%", background: userRole === "admin" ? "#4f46e5" : "#0f172a", color: "white", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: 800, fontSize: "1.1rem" }}>
                  {userRole === "student" ? "S" : userRole === "admin" ? "A" : "T"}
                </div>
                <div>
                  <strong style={{ display: "block", fontSize: "0.95rem", color: "#0f172a" }}>
                    {userInfo?.name || (userRole === "student" ? "Mahasiswa IT Del" : userRole === "admin" ? "Pustakawan Del" : "Tamu Umum")}
                  </strong>
                  <span style={{ fontSize: "0.8rem", color: "#64748b" }}>
                    {userInfo?.prodi || (userRole === "student" ? "S1 Informatika" : userRole === "admin" ? "Staf Perpustakaan" : "Akses Tamu")}
                  </span>
                </div>
              </div>

              <div style={{ display: "flex", flexDirection: "column", gap: "10px", marginBottom: "24px", fontSize: "0.85rem" }}>
                <div style={{ display: "flex", justifyContent: "space-between", padding: "8px 0", borderBottom: "1px dashed #e2e8f0" }}>
                  <span style={{ color: "#64748b" }}>ID / NIM / NIK</span>
                  <strong style={{ color: "#0f172a" }}>{userInfo?.id || (userRole === "guest" ? "GUEST" : "12S23001")}</strong>
                </div>
                <div style={{ display: "flex", justifyContent: "space-between", padding: "8px 0", borderBottom: "1px dashed #e2e8f0" }}>
                  <span style={{ color: "#64748b" }}>Status Akses</span>
                  <span style={{ fontWeight: 600, color: userRole === "guest" ? "#eab308" : "#16a34a" }}>
                    {userRole === "guest" ? "Akses Tamu (FAQ Only)" : "Terverifikasi CIS IT Del"}
                  </span>
                </div>
              </div>

              <button
                type="button"
                onClick={() => {
                  setShowProfileModal(false);
                  onLogout();
                }}
                style={{
                  width: "100%",
                  padding: "11px",
                  background: "#ef4444",
                  color: "white",
                  border: "none",
                  borderRadius: "10px",
                  fontWeight: 600,
                  fontSize: "0.9rem",
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  gap: "8px",
                  boxShadow: "0 4px 12px rgba(239, 68, 68, 0.2)"
                }}
              >
                <span>Keluar / Ganti Akun</span>
              </button>
            </div>
          </div>,
          document.body
        )}
    </>
  );
}