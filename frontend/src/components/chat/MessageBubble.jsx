import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import {
  Bot,
  FileText,
} from "lucide-react";

import MarkdownMessage from "./MarkdownMessage";
import NoveltyCard from "./NoveltyCard";

export default function MessageBubble({
  role,
  content = "",
  citations,
  evidence,
  noveltyAnalysis,
  attachedDocuments = [],
  setActiveCitation,
  setSelectedThesis,
  sources = [],
}) {
  const isAssistant = role === "assistant";
  const isUser = role === "user";

  const handleCitationClick = (citationId) => {
    setActiveCitation?.(citationId);

    const source = sources.find(
      (item) => item.source_id === citationId,
    );

    if (source) {
      setSelectedThesis?.(source);
    }
  };

  return (
    <article
      className={`message ${role}`}
      data-message-role={role}
    >
      {isAssistant && (
        <header className="assistant-message-header">
          <div
            className="assistant-message-avatar"
            aria-hidden="true"
          >
            <Bot size={18} strokeWidth={2} />
          </div>

          <div className="assistant-message-identity">
            <div className="assistant-message-name">
              DELBot
            </div>

            <div className="assistant-message-label">
              Research Intelligence
            </div>
          </div>
        </header>
      )}

      <div className="message-content markdown-body">
        {isUser && attachedDocuments.length > 0 && (
          <div
            className="message-document-list"
            aria-label="Dokumen terlampir"
          >
            {attachedDocuments.map((doc) => (
              <div
                key={
                  doc.document_id ||
                  doc.filename
                }
                className="message-document-pill"
                title={doc.filename}
              >
                <FileText
                  size={14}
                  strokeWidth={2}
                  aria-hidden="true"
                />

                <span>
                  {doc.filename}
                </span>
              </div>
            ))}
          </div>
        )}

        {isAssistant ? (
          <div className="assistant-response-body">
            <MarkdownMessage
              content={content}
              citations={citations}
              evidence={evidence}
              onCitationClick={
                handleCitationClick
              }
            />

            <NoveltyCard
              noveltyAnalysis={
                noveltyAnalysis
              }
            />
          </div>
        ) : (
          <div className="user-message-body">
            <ReactMarkdown
              remarkPlugins={[
                remarkGfm,
              ]}
            >
              {content}
            </ReactMarkdown>
          </div>
        )}
      </div>
    </article>
  );
}