import { useState, useEffect } from "react";
import { BrainCircuit, ShieldCheck } from "lucide-react";

export default function IntroSplash({ onFinish }) {
  const [fadeOut, setFadeOut] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setFadeOut(true);
      setTimeout(() => {
        onFinish?.();
      }, 500);
    }, 1600); // 1.6 detik animasi splash yang cepat & elegan

    return () => clearTimeout(timer);
  }, [onFinish]);

  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100vw",
        height: "100vh",
        background: "#ffffff",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 999999,
        opacity: fadeOut ? 0 : 1,
        transition: "opacity 0.5s cubic-bezier(0.4, 0, 0.2, 1)",
        pointerEvents: fadeOut ? "none" : "all",
        color: "#0f172a"
      }}
    >
      <div
        style={{
          position: "relative",
          zIndex: 10,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          textAlign: "center",
          animation: "splash-scale-in 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards"
        }}
      >
        {/* HARMONIZED BRAND ICON BOX */}
        <div
          style={{
            width: "60px",
            height: "60px",
            borderRadius: "16px",
            background: "#0f172a",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            marginBottom: "16px",
            boxShadow: "0 4px 16px rgba(15, 23, 42, 0.12)"
          }}
        >
          <BrainCircuit size={32} color="#ffffff" />
        </div>

        {/* CLEAN ACADEMIC WORDMARK */}
        <h1
          style={{
            fontSize: "2.2rem",
            fontWeight: "800",
            margin: "0 0 6px 0",
            letterSpacing: "-0.03em",
            color: "#0f172a"
          }}
        >
          DELBot Library Agent
        </h1>

        <div style={{ display: "flex", alignItems: "center", gap: "6px", color: "#64748b", fontSize: "0.9rem", fontWeight: 500 }}>
          <ShieldCheck size={15} color="#0f172a" />
          <span>Sistem Kecerdasan Akademik Perpustakaan IT Del</span>
        </div>
      </div>

      <style>{`
        @keyframes splash-scale-in {
          0% { transform: scale(0.94); opacity: 0; }
          100% { transform: scale(1); opacity: 1; }
        }
      `}</style>
    </div>
  );
}
