import { useState } from "react";
import { KeyRound, ArrowLeft, GraduationCap, Briefcase, Eye, EyeOff } from "lucide-react";

export default function CISLogin({ onBack, onLoginSuccess }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const handleFormSubmit = (e) => {
    e.preventDefault();
    if (!username.trim() || !password.trim()) {
      setErrorMsg("NIM/NIK dan Password wajib diisi!");
      return;
    }

    const cleanUser = username.trim().toLowerCase();
    // Simulate role check based on NIM prefix or username
    if (cleanUser.startsWith("12s") || cleanUser.startsWith("11s") || cleanUser.startsWith("21s") || cleanUser.startsWith("31s")) {
      onLoginSuccess("student", { name: "Budi Pratama", id: username.toUpperCase(), prodi: "S1 Informatika" });
    } else if (cleanUser === "admin" || cleanUser.startsWith("198")) {
      onLoginSuccess("admin", { name: "Ibu Sari (Pustakawan)", id: username.toUpperCase(), prodi: "Staf Perpustakaan" });
    } else {
      // Fallback default student
      onLoginSuccess("student", { name: username, id: "TAMU_DEL", prodi: "Umum" });
    }
  };

  const handlePresetSelect = (role, info) => {
    onLoginSuccess(role, info);
  };

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
          maxWidth: "440px",
          background: "rgba(15, 23, 42, 0.75)",
          backdropFilter: "blur(24px)",
          borderRadius: "28px",
          padding: "36px 30px",
          color: "#ffffff",
          boxShadow: "0 25px 60px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
          border: "1px solid rgba(255, 255, 255, 0.1)",
          position: "relative",
          zIndex: 10
        }}
      >
        {/* BACK BUTTON */}
        <button
          onClick={onBack}
          style={{
            position: "absolute",
            top: "24px",
            left: "24px",
            background: "rgba(255, 255, 255, 0.06)",
            border: "1px solid rgba(255, 255, 255, 0.1)",
            borderRadius: "10px",
            cursor: "pointer",
            color: "#94a3b8",
            display: "flex",
            alignItems: "center",
            gap: "6px",
            fontSize: "0.82rem",
            fontWeight: 600,
            padding: "6px 12px",
            transition: "all 0.2s"
          }}
          className="back-btn"
        >
          <ArrowLeft size={16} />
          <span>Kembali</span>
        </button>

        {/* LOGO IT DEL & TITLE */}
        <div style={{ textAlign: "center", marginTop: "24px", marginBottom: "28px" }}>
          {/* Logo Circle */}
          <div
            style={{
              width: "52px",
              height: "52px",
              borderRadius: "16px",
              background: "linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)",
              color: "white",
              display: "inline-flex",
              alignItems: "center",
              justifyContent: "center",
              fontWeight: 800,
              fontSize: "1.15rem",
              marginBottom: "14px",
              boxShadow: "0 8px 20px rgba(30, 58, 138, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2)"
            }}
          >
            Del
          </div>
          <h2 style={{ fontSize: "1.4rem", fontWeight: 800, margin: "0 0 4px 0", color: "#f8fafc" }}>
            Single Sign-On IT Del
          </h2>
          <span style={{ fontSize: "0.82rem", color: "#94a3b8", fontWeight: 500 }}>
            Gunakan Akun CIS Del untuk melanjutkan ke DELBot
          </span>
        </div>

        {/* LOGIN FORM */}
        <form onSubmit={handleFormSubmit} style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
          {/* username */}
          <div>
            <label style={{ display: "block", fontSize: "0.8rem", fontWeight: 600, color: "#cbd5e1", marginBottom: "6px" }}>
              NIM / NIK / Username
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Contoh: 12S23001"
              style={{
                width: "100%",
                padding: "11px 14px",
                borderRadius: "10px",
                border: "1px solid rgba(255, 255, 255, 0.12)",
                background: "rgba(30, 41, 59, 0.6)",
                color: "#ffffff",
                fontSize: "0.9rem",
                outline: "none",
                transition: "all 0.2s",
                boxSizing: "border-box"
              }}
              className="login-input"
              autoFocus
            />
          </div>

          {/* password */}
          <div>
            <label style={{ display: "block", fontSize: "0.8rem", fontWeight: 600, color: "#cbd5e1", marginBottom: "6px" }}>
              Kata Sandi (Password)
            </label>
            <div style={{ position: "relative" }}>
              <input
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Masukkan password..."
                style={{
                  width: "100%",
                  padding: "11px 42px 11px 14px",
                  borderRadius: "10px",
                  border: "1px solid rgba(255, 255, 255, 0.12)",
                  background: "rgba(30, 41, 59, 0.6)",
                  color: "#ffffff",
                  fontSize: "0.9rem",
                  outline: "none",
                  boxSizing: "border-box"
                }}
                className="login-input"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                style={{
                  position: "absolute",
                  right: "12px",
                  top: "50%",
                  transform: "translateY(-50%)",
                  background: "none",
                  border: "none",
                  cursor: "pointer",
                  color: "#94a3b8",
                  padding: 0
                }}
              >
                {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
          </div>

          {errorMsg && (
            <div style={{ color: "#f87171", fontSize: "0.8rem", fontWeight: 500 }}>
              {errorMsg}
            </div>
          )}

          <button
            type="submit"
            style={{
              width: "100%",
              padding: "12px",
              background: "linear-gradient(135deg, #2563eb 0%, #4f46e5 100%)",
              color: "white",
              border: "none",
              borderRadius: "10px",
              fontWeight: 700,
              fontSize: "0.92rem",
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: "8px",
              boxShadow: "0 6px 20px rgba(37, 99, 235, 0.3)",
              marginTop: "4px"
            }}
            className="submit-btn"
          >
            <KeyRound size={16} />
            <span>Masuk Portal CIS</span>
          </button>
        </form>

        {/* QUICK PRESETS IN DEMO */}
        <div style={{ marginTop: "26px", paddingTop: "20px", borderTop: "1px dashed rgba(255, 255, 255, 0.1)" }}>
          <span style={{ display: "block", fontSize: "0.72rem", fontWeight: 700, color: "#64748b", letterSpacing: "0.06em", textTransform: "uppercase", marginBottom: "12px" }}>
            Uji Cepat Akun Demo (Presets)
          </span>
          <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            {/* Student Preset */}
            <div
              onClick={() => handlePresetSelect("student", { name: "Budi Pratama", id: "12S23001", prodi: "S1 Informatika" })}
              style={{
                display: "flex",
                alignItems: "center",
                gap: "12px",
                padding: "10px 14px",
                borderRadius: "12px",
                border: "1px solid rgba(255, 255, 255, 0.08)",
                background: "rgba(30, 41, 59, 0.4)",
                cursor: "pointer",
                transition: "all 0.2s"
              }}
              className="preset-btn"
            >
              <div style={{ width: "32px", height: "32px", borderRadius: "8px", background: "rgba(56, 189, 248, 0.12)", display: "flex", alignItems: "center", justifyContent: "center" }}>
                <GraduationCap size={18} color="#38bdf8" />
              </div>
              <div style={{ textAlign: "left" }}>
                <strong style={{ display: "block", fontSize: "0.85rem", color: "#f8fafc" }}>Budi Pratama (Mahasiswa)</strong>
                <span style={{ fontSize: "0.73rem", color: "#94a3b8" }}>NIM: 12S23001 · S1 Informatika</span>
              </div>
            </div>

            {/* Librarian Preset */}
            <div
              onClick={() => handlePresetSelect("admin", { name: "Ibu Sari", id: "19850210", prodi: "Staf Perpustakaan" })}
              style={{
                display: "flex",
                alignItems: "center",
                gap: "12px",
                padding: "10px 14px",
                borderRadius: "12px",
                border: "1px solid rgba(255, 255, 255, 0.08)",
                background: "rgba(30, 41, 59, 0.4)",
                cursor: "pointer",
                transition: "all 0.2s"
              }}
              className="preset-btn"
            >
              <div style={{ width: "32px", height: "32px", borderRadius: "8px", background: "rgba(168, 85, 247, 0.12)", display: "flex", alignItems: "center", justifyContent: "center" }}>
                <Briefcase size={18} color="#c084fc" />
              </div>
              <div style={{ textAlign: "left" }}>
                <strong style={{ display: "block", fontSize: "0.85rem", color: "#f8fafc" }}>Ibu Sari (Pustakawan)</strong>
                <span style={{ fontSize: "0.73rem", color: "#94a3b8" }}>NIK: 19850210 · Staf Admin Perpus</span>
              </div>
            </div>
          </div>
        </div>

        <style>{`
          .login-input:focus {
            border-color: #38bdf8 !important;
            box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.15) !important;
          }
          .back-btn:hover {
            background: rgba(255, 255, 255, 0.12) !important;
            color: #ffffff !important;
          }
          .submit-btn:hover {
            opacity: 0.95;
            transform: translateY(-1px);
          }
          .preset-btn:hover {
            border-color: rgba(56, 189, 248, 0.3) !important;
            background: rgba(30, 41, 59, 0.8) !important;
            transform: translateY(-1px);
          }
        `}</style>
      </div>
    </div>
  );
}
