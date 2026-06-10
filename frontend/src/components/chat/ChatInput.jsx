import { useRef } from "react";
import { Paperclip, ArrowUp, FileText, X, Loader2 } from "lucide-react";

export default function ChatInput({
  input,
  setInput,
  sendMessage,
  loading,
  handleFileSelect,
  handleKeyDown,
  activeDocuments,
  selectedFiles = [],
  removeSelectedFile,
  uploadingDocuments,
  removeDocument,
}) {
  const textareaRef = useRef(null);

  const formatFileSize = (size) => {
    if (!size && size !== 0) return "";
    if (size < 1024) return `${size} B`;
    if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`;
    return `${(size / (1024 * 1024)).toFixed(1)} MB`;
  };

  const handleTextareaChange = (e) => {
    setInput(e.target.value);

    const textarea = textareaRef.current;
    if (!textarea) return;

    textarea.style.height = "auto";
    textarea.style.height = `${textarea.scrollHeight}px`;
  };

  return (
    <div className="floating-input-wrapper">
      {uploadingDocuments?.length > 0 && (
        <div className="active-document-bar">
          {uploadingDocuments.map((doc) => (
            <div className="active-document-pill uploading" key={doc.id}>
              <Loader2 size={14} className="spin" />
              <span className="active-document-name">{doc.filename}</span>
              <span className="upload-status">Uploading...</span>
            </div>
          ))}
        </div>
      )}

      {selectedFiles?.length > 0 && (
        <div className="selected-files-bar">
          {selectedFiles.map((file, index) => {
            const isImage = file.type?.startsWith("image/");

            return (
              <div
                key={file.id || `${file.name}-${index}`}
                className={`selected-file-pill ${isImage ? "image" : "document"}`}
              >
                {isImage ? (
                  <img src={file.previewUrl} alt={file.name} className="selected-file-thumb" />
                ) : (
                  <div className="selected-file-icon">
                    <FileText size={14} />
                  </div>
                )}

                <div className="selected-file-meta">
                  <span className="selected-file-name">{file.name}</span>
                  <span className="selected-file-size">{formatFileSize(file.size)}</span>
                </div>

                <button
                  type="button"
                  className="selected-file-remove-btn"
                  onClick={() => removeSelectedFile(index)}
                  aria-label={`Remove ${file.name}`}
                >
                  <X size={12} />
                </button>
              </div>
            );
          })}
        </div>
      )}

      {activeDocuments?.length > 0 && (
        <div className="active-document-bar">
          {activeDocuments.map((doc) => (
            <div className="active-document-pill" key={doc.document_id}>
              <FileText size={14} />
              <span className="active-document-name">{doc.filename}</span>
              <button
                type="button"
                className="document-remove-btn"
                onClick={() => removeDocument(doc.document_id)}
              >
                <X size={12} />
              </button>
            </div>
          ))}
        </div>
      )}

      <div className="smart-actions">
        <button type="button" onClick={() => setInput("Cari research gap terbaru pada bidang NLP healthcare")}>
          Research Gap
        </button>
        <button type="button" onClick={() => setInput("Bandingkan metode CNN dan Transformer")}>
          Compare Methods
        </button>
        <button type="button" onClick={() => setInput("Generate ide judul skripsi AI terbaru")}>
          Thesis Ideas
        </button>
      </div>

      <div className="floating-input">
        <label className="modern-attach">
          <Paperclip size={18} />

          <input
            type="file"
            hidden
            multiple
            accept=".pdf,.png,.jpg,.jpeg,.gif,.webp"
            onChange={handleFileSelect}
          />
        </label>

        <textarea
          ref={textareaRef}
          rows={1}
          placeholder="Ask anything about your research..."
          value={input}
          onChange={handleTextareaChange}
          onKeyDown={handleKeyDown}
        />

        <button className="send-modern-btn" onClick={sendMessage} disabled={loading} type="button">
          <ArrowUp size={18} />
        </button>
      </div>
    </div>
  );
}