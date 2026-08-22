import { useRef, useState, useEffect } from "react";
import { Paperclip, ArrowUp, FileText, X, Loader2, ShieldCheck, Mic, MicOff, Volume2 } from "lucide-react";

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
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef(null);
  const baseInputRef = useRef("");

  useEffect(() => {
    // Inisialisasi Web Speech API (Chrome/Edge/Safari/Opera)
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = "id-ID"; // Bahasa Indonesia

      recognition.onresult = (event) => {
        // Konstruksi total transkripsi ucapan sesi ini dari indeks 0
        let currentSessionTranscript = "";
        for (let i = 0; i < event.results.length; i++) {
          currentSessionTranscript += event.results[i][0].transcript;
        }

        const base = baseInputRef.current.trim();
        const updatedText = base
          ? `${base} ${currentSessionTranscript.trim()}`
          : currentSessionTranscript.trim();

        setInput(updatedText);

        // Auto adjust textarea height
        if (textareaRef.current) {
          textareaRef.current.style.height = "auto";
          textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
        }
      };

      recognition.onerror = (event) => {
        console.error("[SpeechRecognition Error]", event.error);
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
    }
  }, [setInput]);

  const toggleListening = () => {
    if (!recognitionRef.current) {
      alert("Browser Anda belum mendukung input suara langsung. Gunakan Chrome, Edge, atau Safari.");
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      try {
        // Simpan teks dasar sebelum mendengarkan agar tidak terduplikasi
        baseInputRef.current = input || "";
        recognitionRef.current.start();
        setIsListening(true);
      } catch (err) {
        console.error("Failed to start speech recognition:", err);
      }
    }
  };

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

      {/* ============================= */}
      {/* CAPSULE SEARCH BAR */}
      {/* ============================= */}
      <div className="floating-input">
        <label className="modern-attach" title="Lampirkan Dokumen/Foto">
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
          placeholder={isListening ? "Listening... Bicara sekarang dalam Bahasa Indonesia" : "Tanyakan apapun tentang buku, riset, atau skripsi..."}
          value={input}
          onChange={handleTextareaChange}
          onKeyDown={handleKeyDown}
        />

        {/* ============================= */}
        {/* VOICE SPEECH MIC BUTTON */}
        {/* ============================= */}
        <button
          type="button"
          className={`mic-speech-btn ${isListening ? "listening" : ""}`}
          onClick={toggleListening}
          title={isListening ? "Matikan Mikrofon" : "Bicara dengan Suara (STT)"}
          style={{
            background: isListening ? "#ef4444" : "transparent",
            color: isListening ? "#ffffff" : "#64748b",
            border: "none",
            borderRadius: "50%",
            width: "36px",
            height: "36px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            cursor: "pointer",
            transition: "all 0.2s ease",
            marginRight: "6px"
          }}
        >
          {isListening ? <MicOff size={18} className="pulse-icon" /> : <Mic size={18} />}
        </button>

        <button className="send-modern-btn" onClick={sendMessage} disabled={loading} type="button">
          <ArrowUp size={18} />
        </button>
      </div>

      {/* ============================= */}
      {/* SHIELD TRUST FOOTER */}
      {/* ============================= */}
      <div className="input-trust-footer">
        <ShieldCheck size={14} className="shield-icon" />
        <span>DELBot menggunakan sumber akademik resmi perpustakaan & repositori IT Del.</span>
      </div>
    </div>
  );
}