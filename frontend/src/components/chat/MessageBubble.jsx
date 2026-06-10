import React from "react";

import ReactMarkdown from "react-markdown";

import remarkGfm from "remark-gfm";

import { FileText, Image as ImageIcon } from "lucide-react";

import { renderCitationText } from "../../utils/citationParser.jsx";

export default function MessageBubble({
  role,
  content,
  citations,
  evidence,
  attachedDocuments = [],
  attachments = [],
  onImageClick,
  setActiveCitation
}) {
  const attachmentsBlock =
    role === "user" ? (
      <>
        {attachments?.length > 0 && (
          <div className="message-attachments">
            {attachments.map((att) => {
              const isImage = att?.isImage || att?.type?.startsWith?.("image/");

              if (isImage) {
                return (
                  <button
                    key={att.id || att.name}
                    type="button"
                    className="message-image-preview"
                    onClick={() =>
                      onImageClick?.({
                        url: att.serverUrl || att.previewUrl,
                        name: att.name
                      })
                    }
                  >
                    <img
                      src={att.serverUrl || att.previewUrl}
                      alt=""
                      className="message-image"
                    />
                  </button>
                );
              }

              return (
                <div key={att.id || att.name} className="message-document-pill">
                  <FileText size={14} />
                  <span>{att.name}</span>
                </div>
              );
            })}
          </div>
        )}

        {attachedDocuments?.length > 0 && (
          <div className="message-document-list">
            {attachedDocuments.map((doc) => (
              <div
                key={doc.document_id || doc.filename}
                className="message-document-pill"
              >
                <FileText size={14} />
                <span>{doc.filename}</span>
              </div>
            ))}
          </div>
        )}
      </>
    ) : null;

  const markdown = (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        p({ children }) {
          return (
            <p>
              {React.Children.map(children, (child) => {
                if (typeof child === "string") {
                  return renderCitationText(child, setActiveCitation);
                }
                return child;
              })}
            </p>
          );
        },
        li({ children }) {
          return (
            <li>
              {React.Children.map(children, (child) => {
                if (typeof child === "string") {
                  return renderCitationText(child, setActiveCitation);
                }
                return child;
              })}
            </li>
          );
        }
      }}
    >
      {content}
    </ReactMarkdown>
  );

  return (
    <div className={`message ${role}`}>
      {role === "user" ? attachmentsBlock : null}

      <div className={role === "user" ? "message-bubble" : "message-content"}>
        {role === "user" ? <>{content}</> : markdown}
      </div>
    </div>
  );
}

