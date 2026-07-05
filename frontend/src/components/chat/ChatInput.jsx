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

  activeDocuments,

  uploadingDocuments,

  removeDocument,

}) {

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
  // TEXTAREA
  // =====================================

  const textareaRef =
    useRef(null);

  useEffect(() => {

    const textarea =
      textareaRef.current;

    if (!textarea) {

      return;

    }

    textarea.style.height =
      "auto";

    textarea.style.height =
      `${textarea.scrollHeight}px`;

  }, [

    input,

  ]);

  // =====================================
  // AUTO RESIZE
  // =====================================

  const handleTextareaChange =
    (event) => {

      setInput(

        event.target.value

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

                    key={doc.id}

                    className="active-document-pill uploading"

                  >

                    <Loader2

                      size={14}

                      className="spin"

                    />

                    <span className="active-document-name">

                      {doc.filename}

                    </span>

                    <span className="upload-status">

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

                    key={doc.document_id}

                    className="active-document-pill"

                  >

                    <FileText

                      size={14}

                    />

                    <span className="active-document-name">

                      {doc.filename}

                    </span>

                    <button

                      type="button"

                      className="document-remove-btn"

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

            disabled={isGenerating}

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

          placeholder="What would you like to research today?"

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
                {/* ========================= */}
        {/* ACTION BUTTON */}
        {/* ========================= */}

        {

          isGenerating ? (

            <button

              type="button"

              className="send-modern-btn"

              onClick={

                stopGeneration

              }

            >

              <Square

                size={16}

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

                !input.trim()

              }

            >

              <ArrowUp

                size={18}

              />

            </button>

          )

        }

      </div>

    </div>

  );

}