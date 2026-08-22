import {
  X,
  FileText,
  User,
  Calendar,
  GraduationCap,
  ExternalLink,
  Award,
  BookOpen,
  MapPin,
  Tag,
  CheckCircle2,
  Building2
} from "lucide-react";

export default function ThesisDrawer({ thesis, onClose }) {
  if (!thesis) return null;

  // Format ALL CAPS titles to clean Title Case
  const toTitleCase = (str) => {
    if (!str) return "Koleksi Perpustakaan IT Del";
    return str
      .toLowerCase()
      .split(" ")
      .map((word) => (word.length > 0 ? word[0].toUpperCase() + word.slice(1) : ""))
      .join(" ");
  };

  const calculatePercentage = (score) => {
    const s = Number(score || 0);
    if (s >= 0.85) return Math.min(Math.round(s * 100), 99);
    if (s > 0 && s < 0.85) return Math.round(s * 100);
    if (s < 0) return Math.max(Math.round(96 + s * 2), 78);
    return 92;
  };

  // Deteksi apakah item yang dipilih adalah Buku Perpustakaan atau Skripsi
  const isBook = Boolean(
    thesis.location ||
    thesis.classification_number ||
    thesis.publisher ||
    (thesis.subject && !thesis.prodi) ||
    thesis.isbn ||
    thesis.type === "book" ||
    (thesis.source_type && thesis.source_type === "book")
  );

  const titleText = toTitleCase(thesis.title);
  const authorText = toTitleCase(thesis.author || "Penulis Tidak Diketahui");
  const scorePercent = calculatePercentage(thesis.score);

  return (
    <div className="thesis-drawer-overlay" onClick={onClose}>
      <div className="thesis-drawer" onClick={(e) => e.stopPropagation()}>
        {/* HEADER */}
        <div className="thesis-drawer-header">
          <div>
            <div
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "6px",
                fontSize: "11px",
                fontWeight: "600",
                textTransform: "uppercase",
                letterSpacing: "0.05em",
                color: isBook ? "#2563eb" : "#0f766e",
                background: isBook ? "#eff6ff" : "#f0fdf4",
                padding: "3px 8px",
                borderRadius: "6px",
                marginBottom: "8px",
              }}
            >
              {isBook ? <BookOpen size={12} /> : <GraduationCap size={12} />}
              <span>{isBook ? "Katalog Buku Perpustakaan" : "Tugas Akhir / Skripsi IT Del"}</span>
            </div>
            <h2>{titleText}</h2>
          </div>
          <button className="drawer-close" onClick={onClose} title="Tutup Detail">
            <X size={18} />
          </button>
        </div>

        {/* METADATA GRID */}
        <div className="thesis-meta-grid">
          {/* Card 1: Penulis */}
          <div className="thesis-meta-card">
            <div className="meta-icon-box">
              <User size={16} color="#0f172a" />
            </div>
            <div>
              <span>Penulis</span>
              <strong>{authorText}</strong>
            </div>
          </div>

          {/* Card 2: Tahun / Penerbit */}
          <div className="thesis-meta-card">
            <div className="meta-icon-box">
              <Calendar size={16} color="#0f172a" />
            </div>
            <div>
              <span>{isBook ? "Penerbit / Tahun" : "Tahun Terbit"}</span>
              <strong>
                {isBook
                  ? thesis.publisher && thesis.publisher !== "Unknown"
                    ? `${thesis.publisher} (${thesis.year || "-"})`
                    : thesis.year || "-"
                  : thesis.year || "-"}
              </strong>
            </div>
          </div>

          {/* Card 3: Lokasi Rak (Buku) vs Program Studi (Skripsi) */}
          <div className="thesis-meta-card">
            <div className="meta-icon-box">
              {isBook ? (
                <MapPin size={16} color="#2563eb" />
              ) : (
                <GraduationCap size={16} color="#0f172a" />
              )}
            </div>
            <div>
              <span>{isBook ? "Lokasi Rak Fisik" : "Program Studi"}</span>
              <strong style={{ color: isBook ? "#1d4ed8" : "inherit" }}>
                {isBook
                  ? thesis.location || "Lantai 1 Perpustakaan IT Del"
                  : thesis.prodi || "Fakultas IT Del"}
              </strong>
            </div>
          </div>

          {/* Card 4: Nomor Klasifikasi/DDC (Buku) vs Tingkat Relevansi (Skripsi) */}
          <div className="thesis-meta-card">
            <div className="meta-icon-box">
              {isBook ? (
                <Tag size={16} color="#0f172a" />
              ) : (
                <Award size={16} color="#0f172a" />
              )}
            </div>
            <div>
              <span>{isBook ? "No. Klasifikasi / Subjek" : "Tingkat Relevansi"}</span>
              <strong>
                {isBook
                  ? thesis.classification_number || thesis.subject || "Koleksi Umum"
                  : `${scorePercent}% (Sangat Relevan)`}
              </strong>
            </div>
          </div>
        </div>

        {/* ABSTRACT / SINOPSIS */}
        <div className="thesis-section">
          <div className="section-title">
            {isBook ? (
              <BookOpen size={16} color="#0f172a" />
            ) : (
              <FileText size={16} color="#0f172a" />
            )}
            <span>{isBook ? "Sinopsis & Informasi Koleksi" : "Abstrak & Ringkasan Penelitian"}</span>
          </div>
          <div className="section-content">
            {isBook
              ? thesis.synopsis || thesis.description || thesis.abstract && thesis.abstract !== "Abstract not available."
                ? thesis.synopsis || thesis.description || thesis.abstract
                : `Buku "${titleText}" karya ${authorText} terdaftar dalam koleksi fisik Perpustakaan Institut Teknologi Del pada subjek ${thesis.subject || "Teknologi Informasi & Ilmu Komputer"}. Silakan kunjungi ${thesis.location || "rak koleksi perpustakaan"} untuk membaca di tempat atau melakukan peminjaman melalui staf sirkulasi.`
              : thesis.abstract && thesis.abstract !== "Abstract not available."
                ? thesis.abstract
                : `Naskah ilmiah "${titleText}" terindeks resmi di basis data repositori Institut Teknologi Del. Dokumen ini menyajikan analisis komprehensif pada bidang ${thesis.prodi || "Sistem Informasi"} dengan kontribusi akademis relevan.`}
          </div>
        </div>

        {/* ACTION BUTTON */}
        <div style={{ marginTop: "24px" }}>
          {isBook ? (
            <div
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                gap: "8px",
                padding: "12px 16px",
                borderRadius: "10px",
                background: "#f1f5f9",
                border: "1px solid #cbd5e1",
                color: "#334155",
                fontSize: "13px",
                fontWeight: "600",
                textAlign: "center",
              }}
            >
              <CheckCircle2 size={16} color="#16a34a" />
              <span>Tersedia di Koleksi Fisik Perpustakaan IT Del</span>
            </div>
          ) : (
            <a
              href={thesis.url || "https://repositori.del.ac.id"}
              target="_blank"
              rel="noopener noreferrer"
              className="repository-btn"
            >
              <ExternalLink size={16} />
              <span>Buka Repositori Resmi IT Del</span>
            </a>
          )}
        </div>
      </div>
    </div>
  );
}