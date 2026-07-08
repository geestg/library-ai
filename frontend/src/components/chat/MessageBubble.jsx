import {
  useEffect,
  useRef,
  useState,
} from "react";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import {
  Check,
  Copy,
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

  // =====================================
  // MESSAGE TYPE
  // =====================================

  const isAssistant =
    role === "assistant";

  const isUser =
    role === "user";

  // =====================================
  // COPY STATE
  // =====================================

  const [

    isCopied,

    setIsCopied,

  ] = useState(false);

  const copyResetTimerRef =
    useRef(null);

  // =====================================
  // CLEANUP COPY TIMER
  // =====================================

  useEffect(() => {

    return () => {

      if (

        copyResetTimerRef.current

      ) {

        clearTimeout(

          copyResetTimerRef.current

        );

      }

    };

  }, []);

  // =====================================
  // CITATION CLICK
  // =====================================

  const handleCitationClick =
    (citationId) => {

      setActiveCitation?.(
        citationId
      );

      const source =
        sources.find(

          (item) =>

            item.source_id ===
            citationId

        );

      if (source) {

        setSelectedThesis?.(
          source
        );

      }

    };

  // =====================================
  // COPY RESPONSE
  // =====================================

  const handleCopy =
    async () => {

      if (

        !content.trim()

      ) {

        return;

      }

      try {

        await navigator.clipboard.writeText(
          content
        );

        setIsCopied(true);

        if (

          copyResetTimerRef.current

        ) {

          clearTimeout(

            copyResetTimerRef.current

          );

        }

        copyResetTimerRef.current =
          setTimeout(() => {

            setIsCopied(false);

          }, 1800);

      }

      catch (error) {

        console.error(

          "[MESSAGE COPY]",

          error

        );

      }

    };

  // =====================================
  // UI
  // =====================================

  return (

    <article

      className={
        `message ${role}`
      }

      data-message-role={
        role
      }

    >

      {/* ================================= */}
      {/* MESSAGE CONTENT */}
      {/* ================================= */}

      <div
        className="
        message-content
        markdown-body
        "
      >

        {/* =============================== */}
        {/* USER ATTACHMENTS */}
        {/* =============================== */}

        {

          isUser &&

          attachedDocuments.length > 0 && (

            <div

              className="
              message-document-list
              "

              aria-label="
              Dokumen terlampir
              "

            >

              {

                attachedDocuments.map(

                  (doc) => (

                    <div

                      key={

                        doc.document_id
                        ||
                        doc.filename

                      }

                      className="
                      message-document-pill
                      "

                      title={
                        doc.filename
                      }

                    >

                      <FileText

                        size={14}

                        strokeWidth={2}

                        aria-hidden="true"

                      />

                      <span>

                        {
                          doc.filename
                        }

                      </span>

                    </div>

                  )

                )

              }

            </div>

          )

        }

        {/* =============================== */}
        {/* ASSISTANT RESPONSE */}
        {/* =============================== */}

        {

          isAssistant ? (

            <div
              className="
              assistant-response-body
              "
            >

              <MarkdownMessage

                content={
                  content
                }

                citations={
                  citations
                }

                evidence={
                  evidence
                }

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

            <div
              className="
              user-message-body
              "
            >

              <ReactMarkdown

                remarkPlugins={[

                  remarkGfm,

                ]}

              >

                {content}

              </ReactMarkdown>

            </div>

          )

        }

      </div>

      {/* ================================= */}
      {/* ASSISTANT ACTIONS */}
      {/* ================================= */}

      {

        isAssistant &&

        content.trim() && (

          <footer
            className="
            assistant-message-actions
            "
          >

            <button

              type="button"

              className={

                `assistant-action-button${
                  isCopied
                    ? " copied"
                    : ""
                }`

              }

              onClick={
                handleCopy
              }

              aria-label={

                isCopied

                  ? "Jawaban telah disalin"

                  : "Salin jawaban"

              }

              title={

                isCopied

                  ? "Tersalin"

                  : "Salin jawaban"

              }

            >

              {

                isCopied ? (

                  <Check

                    size={15}

                    strokeWidth={2}

                  />

                ) : (

                  <Copy

                    size={15}

                    strokeWidth={2}

                  />

                )

              }

              <span>

                {

                  isCopied

                    ? "Tersalin"

                    : "Salin"

                }

              </span>

            </button>

          </footer>

        )

      }

    </article>

  );

}