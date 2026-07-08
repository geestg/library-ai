import {
  useRef,
  useEffect,
} from "react";

import {
  Paperclip,
  ArrowUp,
  FileText,
  X,
  Loader2,
  Square,
  CircleAlert,
} from "lucide-react";

import {
  ConversationState,
} from "../../hooks/useConversationState";

export default function ChatInput({

  input,

  setInput,

  sendMessage,

  stopGeneration,

  conversationState,

  handleFileUpload,

  handleKeyDown,

  activeDocuments = [],

  uploadingDocuments = [],

  documentError,

  removeDocument,

  clearDocumentError,

  isDocumentDeleting,

}) {

  // =====================================
  // REFS
  // =====================================

  const textareaRef =
    useRef(null);

  const fileInputRef =
    useRef(null);

  // =====================================
  // CONVERSATION STATE
  // =====================================

  const isThinking =

    conversationState ===
    ConversationState.THINKING;

  const isStreaming =

    conversationState ===
    ConversationState.STREAMING;

  const isGenerating =

    isThinking ||
    isStreaming;

  // =====================================
  // DOCUMENT STATE
  // =====================================

  const hasActiveDocuments =

    activeDocuments.length > 0;

  const hasUploadingDocuments =

    uploadingDocuments.length > 0;

  const hasDocumentActivity =

    hasActiveDocuments ||
    hasUploadingDocuments;

  // =====================================
  // TEXTAREA AUTO RESIZE
  // =====================================

  useEffect(() => {

    const textarea =
      textareaRef.current;

    if (!textarea) {

      return;

    }

    textarea.style.height =
      "auto";

    textarea.style.height =
      `${Math.min(
        textarea.scrollHeight,
        180
      )}px`;

  }, [

    input,

  ]);

  // =====================================
  // TEXTAREA CHANGE
  // =====================================

  const handleTextareaChange =
    (event) => {

      setInput(
        event.target.value
      );

    };

  // =====================================
  // OPEN FILE PICKER
  // =====================================

  const openFilePicker = () => {

    if (isGenerating) {

      return;

    }

    fileInputRef.current?.click();

  };

  // =====================================
  // DOCUMENT ERROR LABEL
  // =====================================

  const documentErrorLabel =

    documentError?.filename

      ? `${documentError.message} ${documentError.filename}`

      : documentError?.message;

  // =====================================
  // SEND STATE
  // =====================================

  const canSend =

    Boolean(
      input.trim()
    ) &&

    !isGenerating;

  // =====================================
  // UI
  // =====================================

  return (

    <div className="floating-input-wrapper">

      <div className="composer-shell">

        {/* ================================= */}
        {/* DOCUMENT ERROR */}
        {/* ================================= */}

        {

          documentError && (

            <div

              className="document-error-feedback"

              role="alert"

            >

              <CircleAlert

                size={16}

                className="document-error-icon"

              />

              <span className="document-error-message">

                {documentErrorLabel}

              </span>

              <button

                type="button"

                className="document-error-dismiss"

                aria-label="Dismiss document error"

                onClick={
                  clearDocumentError
                }

              >

                <X size={14} />

              </button>

            </div>

          )

        }

        {/* ================================= */}
        {/* DOCUMENT TRAY */}
        {/* ================================= */}

        {

          hasDocumentActivity && (

            <div className="composer-document-tray">

              {/* ============================= */}
              {/* UPLOADING DOCUMENTS */}
              {/* ============================= */}

              {

                uploadingDocuments.map(

                  (doc) => (

                    <div

                      key={doc.id}

                      className="
                        composer-document-pill
                        uploading
                      "

                    >

                      <span className="composer-document-icon">

                        <Loader2

                          size={15}

                          className="spin"

                        />

                      </span>

                      <span className="composer-document-content">

                        <span className="composer-document-name">

                          {doc.filename}

                        </span>

                        <span className="composer-document-status">

                          Uploading

                        </span>

                      </span>

                    </div>

                  )

                )

              }

              {/* ============================= */}
              {/* ACTIVE DOCUMENTS */}
              {/* ============================= */}

              {

                activeDocuments.map(

                  (doc) => {

                    const isDeleting =

                      isDocumentDeleting?.(
                        doc.document_id
                      ) ?? false;

                    return (

                      <div

                        key={doc.document_id}

                        className={

                          `composer-document-pill${
                            isDeleting
                              ? " deleting"
                              : ""
                          }`

                        }

                      >

                        <span className="composer-document-icon">

                          <FileText size={15} />

                        </span>

                        <span className="composer-document-content">

                          <span className="composer-document-name">

                            {doc.filename}

                          </span>

                          <span className="composer-document-status">

                            {
                              isDeleting

                                ? "Removing"

                                : "Ready"
                            }

                          </span>

                        </span>

                        <button

                          type="button"

                          className="composer-document-remove"

                          disabled={isDeleting}

                          aria-label={

                            isDeleting

                              ? `Removing ${doc.filename}`

                              : `Remove ${doc.filename}`

                          }

                          onClick={() =>

                            removeDocument(
                              doc.document_id
                            )

                          }

                        >

                          {

                            isDeleting ? (

                              <Loader2

                                size={13}

                                className="spin"

                              />

                            ) : (

                              <X size={13} />

                            )

                          }

                        </button>

                      </div>

                    );

                  }

                )

              }

            </div>

          )

        }

        {/* ================================= */}
        {/* COMPOSER */}
        {/* ================================= */}

        <div

          className={

            `floating-input${
              isGenerating
                ? " generating"
                : ""
            }`

          }

        >

          {/* ============================= */}
          {/* TEXTAREA */}
          {/* ============================= */}

          <textarea

            ref={textareaRef}

            rows={1}

            placeholder="Ask about research, theses, methods, or findings..."

            value={input}

            onChange={
              handleTextareaChange
            }

            onKeyDown={
              handleKeyDown
            }

            disabled={
              isGenerating
            }

          />

          {/* ============================= */}
          {/* COMPOSER TOOLBAR */}
          {/* ============================= */}

          <div className="composer-toolbar">

            <div className="composer-toolbar-left">

              <button

                type="button"

                className="composer-tool-button"

                onClick={
                  openFilePicker
                }

                disabled={
                  isGenerating
                }

                aria-label="Attach documents"

              >

                <Paperclip size={18} />

                <span>

                  Attach

                </span>

              </button>

              <input

                ref={fileInputRef}

                type="file"

                hidden

                multiple

                disabled={
                  isGenerating
                }

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

              {

                hasActiveDocuments && (

                  <span className="composer-context-label">

                    {
                      activeDocuments.length
                    }

                    {
                      activeDocuments.length === 1
                        ? " document"
                        : " documents"
                    }

                  </span>

                )

              }

            </div>

            {/* ============================= */}
            {/* ACTION BUTTON */}
            {/* ============================= */}

            {

              isGenerating ? (

                <button

                  type="button"

                  className="
                    send-modern-btn
                    stop
                  "

                  onClick={
                    stopGeneration
                  }

                  aria-label="Stop generation"

                >

                  <Square

                    size={15}

                    fill="currentColor"

                  />

                </button>

              ) : (

                <button

                  type="button"

                  className="send-modern-btn"

                  onClick={
                    sendMessage
                  }

                  disabled={
                    !canSend
                  }

                  aria-label="Send message"

                >

                  <ArrowUp size={19} />

                </button>

              )

            }

          </div>

        </div>

      </div>

    </div>

  );

}