import {
  useRef
} from "react";

import {
  Paperclip,
  ArrowUp,
  FileText,
  X
} from "lucide-react";

export default function ChatInput({

  input,

  setInput,

  sendMessage,

  loading,

  handleFileUpload,

  handleKeyDown,

  activeDocument,

  clearDocument

}) {

  // =====================================
  // TEXTAREA REF
  // =====================================

  const textareaRef =
    useRef(null);

  // =====================================
  // AUTO RESIZE
  // =====================================

  const handleTextareaChange = (
    e
  ) => {

    setInput(
      e.target.value
    );

    const textarea =
      textareaRef.current;

    if (!textarea) {
      return;
    }

    textarea.style.height =
      "auto";

    textarea.style.height =
      `${textarea.scrollHeight}px`;

  };

  // =====================================
  // UI
  // =====================================

  return (

    <div className="floating-input-wrapper">

      {/* ================================= */}
      {/* ACTIVE DOCUMENT */}
      {/* ================================= */}

      {

        activeDocument && (

          <div className="active-document-bar">

            <div className="active-document-left">

              <FileText size={15} />

              <span
                className="active-document-name"
              >

                {

                  activeDocument.filename

                }

              </span>

            </div>

            <button

              className="document-remove-btn"

              onClick={clearDocument}

              type="button"

            >

              <X size={15} />

            </button>

          </div>

        )

      }

      {/* ================================= */}
      {/* SMART ACTIONS */}
      {/* ================================= */}

      <div className="smart-actions">

        <button

          onClick={() =>

            setInput(

              "Cari research gap terbaru pada bidang NLP healthcare"

            )

          }

        >

          Research Gap

        </button>

        <button

          onClick={() =>

            setInput(

              "Bandingkan metode CNN dan Transformer"

            )

          }

        >

          Compare Methods

        </button>

        <button

          onClick={() =>

            setInput(

              "Generate ide judul skripsi AI terbaru"

            )

          }

        >

          Thesis Ideas

        </button>

      </div>

      {/* ================================= */}
      {/* INPUT */}
      {/* ================================= */}

      <div className="floating-input">

        {/* ========================= */}
        {/* ATTACH */}
        {/* ========================= */}

        <label className="modern-attach">

          <Paperclip size={18} />

          <input

            type="file"

            hidden

            multiple

            accept="
            .pdf,
            .doc,
            .docx,
            .ppt,
            .pptx,
            .xls,
            .xlsx,
            .png,
            .jpg,
            .jpeg
            "

            onChange={
              handleFileUpload
            }

          />

        </label>

        {/* ========================= */}
        {/* TEXTAREA */}
        {/* ========================= */}

        <textarea

          ref={textareaRef}

          rows={1}

          placeholder="Ask anything about your research..."

          value={input}

          onChange={
            handleTextareaChange
          }

          onKeyDown={
            handleKeyDown
          }

        />

        {/* ========================= */}
        {/* SEND */}
        {/* ========================= */}

        <button

          className="send-modern-btn"

          onClick={sendMessage}

          disabled={loading}

          type="button"

        >

          <ArrowUp size={18} />

        </button>

      </div>

    </div>

  );

}