import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import {
  FileText,
  FileSpreadsheet,
  Image as ImageIcon,
  FileCode,
  File as FileIcon,
  ChevronDown,
  ChevronUp,
  BrainCircuit,
  Copy,
  Check,
} from "lucide-react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";

export default function MessageBubble({
  role,
  content,
  citations = [],
  sources = [],
  attachedDocuments = [],
  attachments = [],
  data = null,
  onImageClick,
  setActiveCitation,
  setSelectedThesis,
  onActivateMessageSources,
}) {
  const [copied, setCopied] = useState(false);
  const [tableExpanded, setTableExpanded] = useState(false);

  const displaySources = sources?.length > 0 ? sources : citations;

  const handleCopy = (e) => {
    e.stopPropagation();
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleMessageClick = () => {
    if (role === "assistant") {
      onActivateMessageSources?.();
    }
  };

  const renderFileIcon = (file) => {
    if (file.isImage) return <ImageIcon size={14} color="#0284c7" />;
    const name = (file.name || "").toLowerCase();
    if (name.endsWith(".pdf")) return <FileText size={14} color="#ef4444" />;
    if (name.endsWith(".xls") || name.endsWith(".xlsx") || name.endsWith(".csv"))
      return <FileSpreadsheet size={14} color="#10b981" />;
    if (name.endsWith(".json") || name.endsWith(".js") || name.endsWith(".py"))
      return <FileCode size={14} color="#f59e0b" />;
    return <FileIcon size={14} color="#64748b" />;
  };

  const attachmentsBlock =
    (attachedDocuments.length > 0 || attachments.length > 0) && (
      <div className="message-attachments">
        {attachments.map((file) =>
          file.isImage && file.previewUrl ? (
            <button
              key={file.id}
              type="button"
              className="message-image-preview"
              onClick={() => onImageClick?.({ url: file.previewUrl, name: file.name })}
            >
              <img src={file.previewUrl} alt={file.name} className="message-image" />
            </button>
          ) : (
            <div key={file.id} className="attachment-pill">
              {renderFileIcon(file)}
              <span className="attachment-name">{file.name}</span>
            </div>
          )
        )}

        {attachedDocuments.map((doc) => (
          <div key={doc.document_id} className="attachment-pill document-pill">
            <FileText size={14} color="#ef4444" />
            <span className="attachment-name">{doc.filename}</span>
          </div>
        ))}
      </div>
    );

  const processContentWithCitations = (text) => {
    if (!text) return "";
    
    let processed = text;

    // 1. Clean duplicate dataset phrasing (e.g. 'Dataset & Evaluasi: Data yang disarankan:')
    processed = processed.replace(/(?:Dataset & Evaluasi|Saran Data|Dataset)[:\s*]+(?:Data(?:set)?\s+yang\s+disarankan:?\s*)?/gi, "Dataset & Evaluasi: ");

    // 2. Clean and format thesis ideas structure cleanly (no emojis)
    processed = processed.replace(/(?:^|\n)(?:#{1,4}\s*)?(?:💡\s*)?Ide\s*([1-9])\s*:\s*([^\n]+)/gi, (match, num, title) => {
      return `\n\n### Ide ${num}: ${title.trim()}\n\n`;
    });

    // Convert section labels to clean minimal bullet items
    processed = processed.replace(/(?:^|\n)\s*(?:📌\s*)?(?:\*{0,2})Problem(?:\*{0,2}):?\s*(\S[^\n\r]*)/gi, (match, content) => {
      return `\n\n* **Problem:** ${content.trim()}`;
    });
    processed = processed.replace(/(?:^|\n)\s*(?:🔍\s*)?(?:\*{0,2})Research Gap(?:\*{0,2}):?\s*(\S[^\n\r]*)/gi, (match, content) => {
      return `\n\n* **Research Gap:** ${content.trim()}`;
    });
    processed = processed.replace(/(?:^|\n)\s*(?:🚀\s*)?(?:\*{0,2})Solusi & Kebaruan(?:\*{0,2}):?\s*(\S[^\n\r]*)/gi, (match, content) => {
      return `\n\n* **Solusi & Kebaruan:** ${content.trim()}`;
    });
    processed = processed.replace(/(?:^|\n)\s*(?:📊\s*)?(?:\*{0,2})Dataset & Evaluasi(?:\*{0,2}):?\s*(?:Data(?:set)?\s+yang\s+disarankan:?\s*)?(\S[^\n\r]*)/gi, (match, content) => {
      return `\n\n* **Dataset & Evaluasi:** ${content.trim()}`;
    });
    processed = processed.replace(/(?:^|\n)\s*(?:💡\s*|🎯\s*)?(?:Tingkat\s*)?Kesulitan\s*:\s*([^\n\r]+)/gi, (match, diff) => {
      return `\n\n* **Tingkat Kesulitan:** \`${diff.replace(/[`*]/g, "").trim()}\`\n\n---`;
    });

    // 3. Convert citations to safe anchor format
    processed = processed.replace(/\[\s*(\d+)\s*\]\([^)]+\)/g, (match, p1) => {
      return `[${p1}](#cite-${p1})`;
    });
    
    // Then, convert any raw [1] or [ 1 ] that aren't followed by (#cite-
    processed = processed.replace(/\[\s*(\d+)\s*\](?!\(#cite-)/g, (match, p1) => {
      return `[${p1}](#cite-${p1})`;
    });
    
    return processed;
  };

  const processedContent = processContentWithCitations(content);

  const renderMessageBody = () => {
    if (!content) return null;

    const parts = content.split(/(\[PIE_CHART\]|\[BAR_CHART\])/);
    if (parts.length === 1) {
      return (
        <>
          <div className="message-content">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                h1({ children }) {
                  return <h1>{children}</h1>;
                },
                h2({ children }) {
                  return <h2>{children}</h2>;
                },
                h3({ children }) {
                  return <h3>{children}</h3>;
                },
                a({ href, children }) {
                  if (href && href.startsWith("#cite-")) {
                    const citeId = href.replace("#cite-", "");
                    const numIndex = Number(citeId);
                    const matchedCitation =
                      displaySources.find(
                        (c) =>
                          String(c.source_id) === citeId ||
                          String(c.id) === citeId ||
                          String(c.index) === citeId
                      ) || displaySources[numIndex - 1];

                    return (
                      <button
                        type="button"
                        className="citation-badge"
                        onClick={(e) => {
                          e.stopPropagation();
                          onActivateMessageSources?.();
                          if (matchedCitation) {
                            setActiveCitation?.(matchedCitation.source_id || citeId);
                          }
                        }}
                        title={
                          matchedCitation
                            ? `[Kutipan #${citeId}] ${matchedCitation.title || matchedCitation.author || "Lihat Repositori IT Del"}`
                            : `Buka Referensi Kutipan #${citeId}`
                        }
                      >
                        [{citeId}]
                      </button>
                    );
                  }

                  return (
                    <a href={href} target="_blank" rel="noopener noreferrer">
                      {children}
                    </a>
                  );
                },
              }}
            >
              {processedContent}
            </ReactMarkdown>
          </div>
          {data && data.length > 0 && renderVisuals()}
        </>
      );
    }

    return (
      <>
        {parts.map((part, index) => {
          if (part === "[PIE_CHART]" || part === "[BAR_CHART]") {
            return data && data.length > 0 ? (
              <div key={index}>{renderVisuals()}</div>
            ) : null;
          }

          if (!part.trim()) return null;

          return (
            <div className="message-content" key={index}>
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  h1({ children }) {
                    return <h1>{children}</h1>;
                  },
                  h2({ children }) {
                    return <h2>{children}</h2>;
                  },
                  h3({ children }) {
                    return <h3>{children}</h3>;
                  },
                  a({ href, children }) {
                    if (href && href.startsWith("#cite-")) {
                      const citeId = href.replace("#cite-", "");
                      const numIndex = Number(citeId);
                      const matchedCitation =
                        displaySources.find(
                          (c) =>
                            String(c.source_id) === citeId ||
                            String(c.id) === citeId ||
                            String(c.index) === citeId
                        ) || displaySources[numIndex - 1];

                      return (
                        <button
                          type="button"
                          className="citation-badge"
                          onClick={(e) => {
                            e.stopPropagation();
                            onActivateMessageSources?.();
                            if (matchedCitation) {
                              setActiveCitation?.(matchedCitation.source_id || citeId);
                            }
                          }}
                          title={
                            matchedCitation
                              ? `[Kutipan #${citeId}] ${matchedCitation.title || matchedCitation.author || "Lihat Repositori IT Del"}`
                              : `Buka Referensi Kutipan #${citeId}`
                          }
                        >
                          [{citeId}]
                        </button>
                      );
                    }

                    return (
                      <a href={href} target="_blank" rel="noopener noreferrer">
                        {children}
                      </a>
                    );
                  },
                }}
              >
                {part}
              </ReactMarkdown>
            </div>
          );
        })}
      </>
    );
  };

  const renderVisuals = () => {
    if (!data || !Array.isArray(data) || data.length === 0) return null;
    const firstRow = data[0];
    let stringKeys = Object.keys(firstRow).filter((k) => typeof firstRow[k] === "string");
    if (stringKeys.length === 0) stringKeys = [Object.keys(firstRow)[0]];
    const xAxisKey = stringKeys[0];
    const numericKeys = Object.keys(firstRow).filter(
      (k) => typeof firstRow[k] === "number" && k !== xAxisKey
    );
    if (numericKeys.length === 0) return null;

    // Detect if this is sirkulasi status composition data (useful for PieChart)
    const isSirkulasiStatus = data.some((row) => row.Status !== undefined);

    if (isSirkulasiStatus) {
      const COLORS = {
        "Sudah Dikembalikan": "#10b981",
        "Belum Jatuh Tempo": "#3b82f6",
        "Lewat Jatuh Tempo": "#ef4444",
      };
      const defaultColors = ["#1e3a8a", "#0284c7", "#f59e0b"];

      return (
        <div
          style={{
            width: "100%",
            height: 320,
            marginTop: "16px",
            marginBottom: "16px",
            padding: "16px",
            background: "#f8fafc",
            borderRadius: "12px",
            border: "1px solid #e2e8f0",
          }}
        >
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="45%"
                innerRadius={60}
                outerRadius={90}
                paddingAngle={4}
                dataKey={numericKeys[0]}
                nameKey="Status"
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(1)}%`}
              >
                {data.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[entry.Status] || defaultColors[index % defaultColors.length]}
                  />
                ))}
              </Pie>
              <Tooltip formatter={(value) => [`${value} Buku`]} />
              <Legend verticalAlign="bottom" height={36} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      );
    }

    // Default: BarChart
    return (
      <div
        style={{
          width: "100%",
          height: 300,
          marginTop: "16px",
          marginBottom: "16px",
          padding: "16px",
          background: "#f8fafc",
          borderRadius: "12px",
          border: "1px solid #e2e8f0",
        }}
      >
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 10, right: 10, left: -10, bottom: 40 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
            <XAxis dataKey={xAxisKey} tick={{ fontSize: 11, fill: "#64748b" }} interval={0} angle={-15} textAnchor="end" />
            <YAxis tick={{ fontSize: 11, fill: "#64748b" }} />
            <Tooltip contentStyle={{ borderRadius: "8px", border: "1px solid #e2e8f0", fontSize: "12px" }} />
            {numericKeys.map((key, i) => (
              <Bar key={key} dataKey={key} fill={i === 0 ? "#1e3a8a" : "#0284c7"} radius={[4, 4, 0, 0]} />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </div>
    );
  };

  const renderTable = () => {
    if (!data || !Array.isArray(data) || data.length === 0) return null;

    // Suppress table rendering for summary/insight datasets that already have visual charts
    const isSummaryData = data.some(
      (row) =>
        row.Status !== undefined ||
        (row["Program Studi"] !== undefined && row["Jumlah Kunjungan"] !== undefined)
    );
    if (isSummaryData) return null;

    const columns = Object.keys(data[0]);
    const displayData = tableExpanded ? data : data.slice(0, 5);

    return (
      <div className="table-container" style={{ marginTop: "16px" }}>
        <div style={{ overflowX: "auto" }}>
          <table className="admin-table">
            <thead>
              <tr>
                {columns.map((col) => (
                  <th key={col}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {displayData.map((row, idx) => (
                <tr key={idx}>
                  {columns.map((col) => (
                    <td key={col}>{row[col] !== null ? String(row[col]) : "-"}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {data.length > 5 && (
          <button
            type="button"
            className="table-expand-btn"
            onClick={() => setTableExpanded(!tableExpanded)}
          >
            {tableExpanded ? (
              <>
                <span>Sembunyikan Baris</span>
                <ChevronUp size={14} />
              </>
            ) : (
              <>
                <span>Lihat Semua {data.length} Baris</span>
                <ChevronDown size={14} />
              </>
            )}
          </button>
        )}
      </div>
    );
  };

  const timeStr = new Date().toLocaleTimeString("id-ID", { hour: "2-digit", minute: "2-digit" });

  return (
    <div
      className={`message ${role}`}
      onClick={handleMessageClick}
      style={{ cursor: role === "assistant" ? "pointer" : "default" }}
    >
      {role === "user" ? attachmentsBlock : null}

      {role === "user" && (
        <div className="user-bubble-wrapper">
          <div className="user-bubble-column">
            <div className="message-bubble">
              <span className="user-bubble-text">{content}</span>
            </div>
            <div className="user-bubble-timestamp">{timeStr}</div>
          </div>
        </div>
      )}

      {role === "assistant" && (
        <div className="assistant-card-wrapper">
          <div className="assistant-avatar-header">
            <div className="assistant-mini-avatar">
              <BrainCircuit size={14} color="#ffffff" />
            </div>
            <div className="assistant-title-meta">
              <span className="assistant-name">DELBot</span>
              <span className="assistant-time">{timeStr}</span>
            </div>
          </div>

          <div className="message-content-card">
            {renderMessageBody()}
            {data && data.length > 0 && renderTable()}

            {/* SUBTLE HOVER COPY BUTTON */}
            <div className="assistant-actions-subtle">
              <button
                type="button"
                className="action-btn-copy-subtle"
                onClick={handleCopy}
                title="Salin Teks Jawaban"
              >
                {copied ? <Check size={12} color="#10b981" /> : <Copy size={12} />}
                <span>{copied ? "Tersalin" : "Salin"}</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
