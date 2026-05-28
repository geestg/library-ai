import {
  useRef
} from "react";

import {
  Paperclip,
  CheckCircle2,
  ArrowUp
} from "lucide-react";


export default function ChatInput({

  input,

  setInput,

  sendMessage,

  loading,

  uploadedFiles,

  handleFileUpload,

  handleKeyDown

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

    if (!textarea) return;

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

      {/* ========================= */}
      {/* FILES */}
      {/* ========================= */}

      {

        uploadedFiles.length > 0 && (

          <div className="floating-files">

            {

              uploadedFiles.map(
                (file, idx) => (

                  <div
                    key={idx}
                    className="modern-file-pill"
                  >

                    <CheckCircle2
                      size={14}
                    />

                    {file.name}

                  </div>
                )
              )
            }

          </div>
        )
      }

      {/* ========================= */}
      {/* SMART ACTIONS */}
      {/* ========================= */}

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

      {/* ========================= */}
      {/* INPUT */}
      {/* ========================= */}

      <div className="floating-input">

        {/* ======================= */}
        {/* ATTACH */}
        {/* ======================= */}

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
            .xlsx
            "

            onChange={
              handleFileUpload
            }
          />

        </label>

        {/* ======================= */}
        {/* TEXTAREA */}
        {/* ======================= */}

        <textarea

          ref={textareaRef}

          rows={1}

          placeholder="
          Ask anything about your research...
          "

          value={input}

          onChange={
            handleTextareaChange
          }

          onKeyDown={
            handleKeyDown
          }

        />

        {/* ======================= */}
        {/* SEND */}
        {/* ======================= */}

        <button

          className="send-modern-btn"

          onClick={sendMessage}

          disabled={loading}

        >

          <ArrowUp size={18} />

        </button>

      </div>

    </div>
  );
}