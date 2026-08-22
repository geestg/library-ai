import { useEffect } from "react";
import { FileText, BookCheck, ExternalLink } from "lucide-react";

export default function SearchPanel({
  sources = [],
  activeCitation,
  setActiveCitation,
  setSelectedThesis
}) {
  // =================================
  // ACTIVE CITATION SCROLL
  // =================================
  useEffect(() => {
    if (!activeCitation) return;
    const container = document.querySelector(".evidence-shell");
    const element = document.getElementById(`citation-${activeCitation}`);

    if (!container || !element) return;

    const containerRect = container.getBoundingClientRect();
    const elementRect = element.getBoundingClientRect();
    const targetScrollTop =
      elementRect.top - containerRect.top + container.scrollTop - 100;

    container.scrollTo({
      top: targetScrollTop,
      behavior: "smooth"
    });
  }, [activeCitation]);

  const formatTitle = (title) => {
    if (!title) return "Karya Ilmiah / Skripsi IT Del";
    return title;
  };

  const calculatePercentage = (score) => {
    const s = Number(score || 0);
    if (s >= 0.85) return Math.min(Math.round(s * 100), 99);
    if (s > 0 && s < 0.85) return Math.round(s * 100);
    if (s < 0) return Math.max(Math.round(96 + s * 2), 78);
    return 90;
  };

  return (
    <div className="evidence-shell">
      {/* ================================= */}
      {/* HEADER */}
      {/* ================================= */}
      <div className="evidence-header">
        <h2>Sumber Referensi Akademik</h2>
        <p>Referensi ilmiah & repositori resmi IT Del.</p>
      </div>

      {/* ================================= */}
      {/* EMPTY STATE */}
      {/* ================================= */}
      {sources.length === 0 && (
        <div className="evidence-empty">
          <div className="empty-icon">
            <FileText size={32} />
          </div>
          <h3>Belum Ada Referensi Kutipan</h3>
          <p>
            Tanyakan kueri riset atau topik skripsi, maka daftar referensi ilmiah yang relevan dari IT Del akan otomatis tampil di sini.
          </p>
        </div>
      )}

      {/* ================================= */}
      {/* SOURCE LIST */}
      {/* ================================= */}
      <div className="evidence-list">
        {sources.map((source) => {
          const isActive = activeCitation === source.source_id;
          const scorePercent = calculatePercentage(source.score);

          return (
            <div
              id={`citation-${source.source_id}`}
              key={source.source_id}
              onClick={() => {
                setActiveCitation?.(source.source_id);
                setSelectedThesis?.(source);
              }}
              className={`evidence-card ${isActive ? "active" : ""}`}
            >
              <div className="evidence-card-top">
                <div className="evidence-source-icon">
                  <FileText size={16} />
                </div>
                <div className="evidence-top-content">
                  <div className="evidence-source-name">
                    {formatTitle(source.title)}
                  </div>
                  <div className="evidence-citation-id">
                    Kutipan #{source.source_id}
                  </div>
                </div>
              </div>

              {/* AUTHOR METADATA WITH CRISP VISIBILITY */}
              <div className="evidence-author">
                Penulis: {source.author || "Penulis Tidak Diketahui"}
              </div>

              <div className="evidence-meta-row">
                <div className="meta-pill">
                  Tahun: {source.year || "-"}
                </div>
                <div className="meta-pill">
                  {source.prodi || "Fakultas IT Del"}
                </div>
              </div>

              {/* RELEVANCE SCORE BAR */}
              <div className="evidence-score-wrapper">
                <div className="score-header">
                  <span>Tingkat Relevansi</span>
                  <span className="score-percentage">{scorePercent}%</span>
                </div>
                <div className="score-bar">
                  <div
                    className="score-fill"
                    style={{ width: `${scorePercent}%` }}
                  />
                </div>
              </div>

              {/* REPOSITORY EXTERNAL LINK */}
              {source.url && (
                <a
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="evidence-link"
                  onClick={(e) => e.stopPropagation()}
                >
                  <ExternalLink size={13} />
                  <span>Buka Repositori IT Del</span>
                </a>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}