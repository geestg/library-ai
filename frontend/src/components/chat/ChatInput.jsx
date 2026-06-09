import {
  useRef
} from "react";

import {
  Paperclip,
  ArrowUp,
  FileText,
  X,
  Loader2
} from "lucide-react";

export default function ChatInput({

  input,

  setInput,

  sendMessage,

  loading,

  handleFileUpload,

  handleKeyDown,

  activeDocuments,

  uploadingDocuments,

  removeDocument

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
      {/* UPLOADING DOCUMENTS */}
      {/* ================================= */}

      {

        uploadingDocuments?.length > 0 && (

          <div className="active-document-bar">

            {

              uploadingDocuments.map(

                (doc) => (

                  <div

                    className="
                    active-document-pill
                    uploading
                    "

                    key={
                      doc.id
                    }

                  >

                    <Loader2
                      size={14}
                      className="spin"
                    />

                    <span
                      className="
                      active-document-name
                      "
                    >

                      {
                        doc.filename
                      }

                    </span>

                    <span
                      className="
                      upload-status
                      "
                    >

                      Uploading...

                    </span>

                  </div>

                )

              )

            }

          </div>

        )

      }

      {/* ================================= */}
      {/* ACTIVE DOCUMENTS */}
      {/* ================================= */}

      {

        activeDocuments?.length > 0 && (

          <div className="active-document-bar">

            {

              activeDocuments.map(

                (doc) => (

                  <div

                    className="
                    active-document-pill
                    "

                    key={
                      doc.document_id
                    }

                  >

                    <FileText
                      size={14}
                    />

                    <span
                      className="
                      active-document-name
                      "
                    >

                      {
                        doc.filename
                      }

                    </span>

                    <button

                      type="button"

                      className="
                      document-remove-btn
                      "

                      onClick={() =>

                        removeDocument(
                          doc.document_id
                        )

                      }

                    >

                      <X
                        size={12}
                      />

                    </button>

                  </div>

                )

              )

            }

          </div>

        )

      }

      {/* ================================= */}
      {/* SMART ACTIONS */}
      {/* ================================= */}

      <div className="smart-actions">

        <button

          type="button"

          onClick={() =>

            setInput(

              "Cari research gap terbaru pada bidang NLP healthcare"

            )

          }

        >

          Research Gap

        </button>

        <button

          type="button"

          onClick={() =>

            setInput(

              "Bandingkan metode CNN dan YOLO"

            )

          }

        >

          Compare Methods

        </button>

        <button

          type="button"

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

          <Paperclip
            size={18}
          />

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
            .csv,
            .txt,
            .png,
            .jpg,
            .jpeg,
            .webp
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

          onClick={
            sendMessage
          }

          disabled={
            loading
          }

          type="button"

        >

          <ArrowUp
            size={18}
          />

        </button>

      </div>

    </div>

  );

}