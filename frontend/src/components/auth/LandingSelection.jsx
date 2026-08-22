import { useState } from "react";
import { BrainCircuit, GraduationCap, Briefcase, KeyRound, ArrowRight, ShieldCheck } from "lucide-react";
import CISLogin from "./CISLogin";

export default function LandingSelection({ onLoginSuccess }) {
  const [showCISLogin, setShowCISLogin] = useState(false);

  if (showCISLogin) {
    return <CISLogin onBack={() => setShowCISLogin(false)} onLoginSuccess={onLoginSuccess} />;
  }

  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        background: "#090d16",
        backgroundImage: `
          radial-gradient(circle at 20% 20%, rgba(56, 189, 248, 0.12) 0%, transparent 40%),
          radial-gradient(circle at 80% 80%, rgba(99, 102, 241, 0.14) 0%, transparent 40%)
        `,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        color: "#ffffff",
        fontFamily: "'Inter', system-ui, -apple-system, sans-serif",
        padding: "20px",
        boxSizing: "border-box",
        position: "relative",
        overflow: "hidden"
      }}
    >
      {/* AMBIENT BACKGROUND DECORATION GRID */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: "linear-gradient(to right, rgba(255, 255, 255, 0.02) 1px, transparent 1px), linear-gradient(to bottom, rgba(255, 255, 255, 0.02) 1px, transparent 1px)",
          backgroundSize: "32px 32px",
          pointerEvents: "none"
        }}
      />

      <div
        style={{
          width: "100%",
          maxWidth: "500px",
          textAlign: "center",
          background: "rgba(15, 23, 42, 0.7)",
          backdropFilter: "blur(24px)",
          borderRadius: "28px",
          border: "1px solid rgba(255, 255, 255, 0.1)",
          padding: "44px 36px",
          boxShadow: "0 25px 60px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
          animation: "fade-scale-in 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards",
          position: "relative",
          zIndex: 10
        }}
      >
        {/* IT DEL EMBLEM BADGE */}
        <div style={{ display: "inline-flex", alignItems: "center", gap: "6px", background: "rgba(56, 189, 248, 0.1)", border: "1px solid rgba(56, 189, 248, 0.25)", color: "#38bdf8", padding: "5px 14px", borderRadius: "999px", fontSize: "0.73rem", fontWeight: 700, letterSpacing: "0.06em", textTransform: "uppercase", marginBottom: "20px" }}>
          <ShieldCheck size={14} color="#38bdf8" />
          <span>INSTITUT TEKNOLOGI DEL</span>
          <span style={{ opacity: 0.5 }}>•</span>
          <span>CIS SSO PORTAL</span>
        </div>

        {/* BRANDING */}
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", marginBottom: "32px" }}>
          <div
            style={{
              width: "68px",
              height: "68px",
              borderRadius: "20px",
              background: "linear-gradient(135deg, #0284c7 0%, #4f46e5 100%)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              marginBottom: "18px",
              boxShadow: "0 10px 25px rgba(2, 132, 199, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.2)"
            }}
          >
            <BrainCircuit size={34} color="#ffffff" />
          </div>
          <h1 style={{ fontSize: "2.1rem", fontWeight: 800, margin: "0 0 8px 0", letterSpacing: "-0.03em", background: "linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
            DELBot Library Agent
          </h1>
          <p style={{ color: "#94a3b8", fontSize: "0.92rem", margin: 0, fontWeight: 500, lineHeight: 1.4 }}>
            Sistem Informasi & Kecerdasan Buatan Perpustakaan IT Del
          </p>
        </div>

        {/* 2 CORE SELECTIONS */}
        <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
          {/* 1. Mahasiswa IT Del Portal */}
          <div
            onClick={() => onLoginSuccess("student", { name: "Budi Pratama", id: "12S23001", prodi: "S1 Informatika" })}
            style={{
              background: "linear-gradient(135deg, rgba(2, 132, 199, 0.15) 0%, rgba(56, 189, 248, 0.1) 100%)",
              border: "1px solid rgba(56, 189, 248, 0.3)",
              borderRadius: "18px",
              padding: "20px",
              textAlign: "left",
              cursor: "pointer",
              transition: "all 0.25s cubic-bezier(0.16, 1, 0.3, 1)",
              display: "flex",
              alignItems: "center",
              gap: "16px",
              position: "relative"
            }}
            className="hover-card-student"
          >
            <div
              style={{
                width: "48px",
                height: "48px",
                borderRadius: "14px",
                background: "rgba(56, 189, 248, 0.18)",
                border: "1px solid rgba(56, 189, 248, 0.3)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                flexShrink: 0
              }}
            >
              <GraduationCap size={24} color="#38bdf8" />
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "3px" }}>
                <h3 style={{ margin: 0, fontSize: "1.05rem", fontWeight: 700, color: "#f8fafc" }}>
                  Portal Mahasiswa IT Del
                </h3>
                <span style={{ fontSize: "0.68rem", background: "rgba(56, 189, 248, 0.2)", color: "#38bdf8", padding: "2px 8px", borderRadius: "999px", fontWeight: 700 }}>
                  Budi Pratama
                </span>
              </div>
              <p style={{ margin: 0, fontSize: "0.82rem", color: "#94a3b8", lineHeight: "1.35" }}>
                RAG skripsi & ide riset, katalog buku, FAQ kampus, & rekomendasi bacaan.
              </p>
            </div>
            <ArrowRight size={18} color="#38bdf8" style={{ marginLeft: "auto", transition: "transform 0.2s" }} className="card-arrow" />
          </div>

          {/* 2. Pengelola Perpustakaan Portal */}
          <div
            onClick={() => onLoginSuccess("admin", { name: "Ibu Sari", id: "19850210", prodi: "Staf Perpustakaan" })}
            style={{
              background: "linear-gradient(135deg, rgba(79, 70, 229, 0.18) 0%, rgba(147, 51, 234, 0.15) 100%)",
              border: "1px solid rgba(99, 102, 241, 0.35)",
              borderRadius: "18px",
              padding: "20px",
              textAlign: "left",
              cursor: "pointer",
              transition: "all 0.25s cubic-bezier(0.16, 1, 0.3, 1)",
              display: "flex",
              alignItems: "center",
              gap: "16px",
              position: "relative"
            }}
            className="hover-card-admin"
          >
            <div
              style={{
                width: "48px",
                height: "48px",
                borderRadius: "14px",
                background: "linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                flexShrink: 0,
                boxShadow: "0 6px 16px rgba(79, 70, 229, 0.3)"
              }}
            >
              <Briefcase size={22} color="#ffffff" />
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "3px" }}>
                <h3 style={{ margin: 0, fontSize: "1.05rem", fontWeight: 700, color: "#ffffff" }}>
                  Pengelola Perpustakaan
                </h3>
                <span style={{ fontSize: "0.68rem", background: "rgba(168, 85, 247, 0.25)", color: "#c084fc", padding: "2px 8px", borderRadius: "999px", fontWeight: 700 }}>
                  Ibu Sari
                </span>
              </div>
              <p style={{ margin: 0, fontSize: "0.82rem", color: "#c7d2fe", lineHeight: "1.35" }}>
                Data sirkulasi peminjaman, log pengunjung, laporan, & sinkronisasi data.
              </p>
            </div>
            <ArrowRight size={18} color="#c7d2fe" style={{ marginLeft: "auto", transition: "transform 0.2s" }} className="card-arrow" />
          </div>
        </div>

        {/* CUSTOM CREDENTIAL TOGGLE */}
        <div style={{ marginTop: "22px" }}>
          <button
            type="button"
            onClick={() => setShowCISLogin(true)}
            style={{
              background: "none",
              border: "none",
              color: "#94a3b8",
              fontSize: "0.82rem",
              fontWeight: 600,
              cursor: "pointer",
              display: "inline-flex",
              alignItems: "center",
              gap: "6px",
              padding: "6px 12px",
              borderRadius: "8px",
              transition: "all 0.2s"
            }}
            className="custom-login-btn"
          >
            <KeyRound size={14} color="#38bdf8" />
            <span>Masuk dengan Kredensial Akun CIS Kustom</span>
          </button>
        </div>

        {/* BOTTOM DISCLAIMER */}
        <div style={{ marginTop: "24px", fontSize: "0.78rem", color: "#64748b", fontWeight: 500, lineHeight: 1.4 }}>
          Sistem Terotentikasi Single Sign-On (SSO) Institut Teknologi Del.
        </div>

        {/* HOVER EFFECT CSS INJECTED */}
        <style>{`
          @keyframes fade-scale-in {
            0% { transform: scale(0.96); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
          }
          .hover-card-student:hover {
            background: linear-gradient(135deg, rgba(2, 132, 199, 0.25) 0%, rgba(56, 189, 248, 0.18) 100%) !important;
            border-color: rgba(56, 189, 248, 0.6) !important;
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(2, 132, 199, 0.2);
          }
          .hover-card-student:hover .card-arrow {
            transform: translateX(4px);
            color: #38bdf8 !important;
          }
          .hover-card-admin:hover {
            background: linear-gradient(135deg, rgba(79, 70, 229, 0.3) 0%, rgba(147, 51, 234, 0.25) 100%) !important;
            border-color: rgba(129, 140, 248, 0.6) !important;
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(79, 70, 229, 0.25);
          }
          .hover-card-admin:hover .card-arrow {
            transform: translateX(4px);
            color: #ffffff !important;
          }
          .custom-login-btn:hover {
            color: #ffffff !important;
            background: rgba(255, 255, 255, 0.05) !important;
          }
        `}</style>
      </div>
    </div>
  );
}
