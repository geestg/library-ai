import {
  useState,
  useEffect
} from "react";

import {
  API_BASE_URL
} from "../../services/api";

import MessageBubble from "./MessageBubble";
import ChatHero from "./ChatHero";
import ChatInput from "./ChatInput";
import ThinkingIndicator from "./ThinkingIndicator";

export default function ChatWindow({

  messages = [],

  setMessages,

  sources = [],

  setSources,

  setEvidence,

  setEvidenceMatrix,

  setGapAnalysis,

  activeCitation,

  setActiveCitation,

  setSelectedThesis

}) {

  // =====================================
  // CHAT STATE
  // =====================================

  const [input, setInput] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  // =====================================
  // ACTIVE DOCUMENTS
  // =====================================

  const [

    activeDocuments,

    setActiveDocuments

  ] = useState([]);

  // =====================================
  // UPLOADING DOCUMENTS
  // =====================================

  const [

    uploadingDocuments,

    setUploadingDocuments

  ] = useState([]);

  // =====================================
  // AUTO SCROLL
  // =====================================

  useEffect(() => {

    const container =
      document.querySelector(
        ".modern-messages"
      );

    if (!container) {
      return;
    }

    container.scrollTo({

      top:
        container.scrollHeight,

      behavior:
        "smooth"

    });

  }, [

    messages,

    loading

  ]);

  // =====================================
  // REMOVE DOCUMENT
  // =====================================

  const removeDocument = (
    documentId
  ) => {

    setActiveDocuments(

      prev =>

        prev.filter(

          doc =>

            doc.document_id !==
            documentId

        )

    );

  };

  // =====================================
  // CLEAR DOCUMENTS
  // =====================================

  const clearDocuments = () => {

    setActiveDocuments([]);

    localStorage.removeItem(
      "delbot_documents"
    );

  };

  // =====================================
  // FILE UPLOAD
  // =====================================

  const handleFileUpload =
    async (e) => {

      const files =
        Array.from(
          e.target.files || []
        );

      if (!files.length) {
        return;
      }

      for (const file of files) {

        const uploadId =
          `${Date.now()}-${file.name}`;

        setUploadingDocuments(

          prev => [

            ...prev,

            {

              id:
                uploadId,

              filename:
                file.name

            }

          ]

        );

        try {

          const formData =
            new FormData();

          formData.append(
            "file",
            file
          );

          const response =
            await fetch(

              `${API_BASE_URL}/upload-pdf`,

              {

                method:
                  "POST",

                body:
                  formData

              }

            );

          if (
            !response.ok
          ) {

            throw new Error(
              `Upload failed (${response.status})`
            );

          }

          const data =
            await response.json();

          setUploadingDocuments(

            prev =>

              prev.filter(

                item =>

                  item.id !==
                  uploadId

              )

          );

          if (
            data.document_id
          ) {

            setActiveDocuments(

              prev => [

                ...prev,

                {

                  document_id:
                    data.document_id,

                  filename:
                    data.filename,

                  pages:
                    data.pages || 0,

                  chunks:
                    data.chunks || 0,

                  file_type:
                    data.file_type || "unknown"

                }

              ]

            );

          }

        } catch (error) {

          console.error(
            "UPLOAD ERROR:",
            error
          );

          setUploadingDocuments(

            prev =>

              prev.filter(

                item =>

                  item.id !==
                  uploadId

              )

          );

        }

      }

      e.target.value = "";

    };

  // =====================================
  // SEND MESSAGE
  // =====================================

  const sendMessage =
    async () => {

      if (
        !input.trim()
      ) {
        return;
      }

      const finalInput =
        input.trim();

      // ===============================
      // RESET RIGHT PANEL
      // ===============================

      setActiveCitation(
        null
      );

      setSources([]);

      setEvidence({});

      setEvidenceMatrix({});

      setGapAnalysis({});

      // ===============================
      // ADD CHAT MESSAGE
      // ===============================

      setMessages(

        prev => [

          ...prev,

          {

            role:
              "user",

            content:
              finalInput,

            attachedDocuments:
              activeDocuments

          },

          {

            role:
              "assistant",

            content:
              ""

          }

        ]

      );

      setInput("");

      const textarea =
        document.querySelector(
          ".floating-input textarea"
        );

      if (textarea) {

        textarea.style.height =
          "auto";

      }

      setLoading(true);

      try {

        const response =
          await fetch(

            `${API_BASE_URL}/api/research/research-analysis`,

            {

              method:
                "POST",

              headers: {

                "Content-Type":
                  "application/json"

              },

              body:
                JSON.stringify({

                  query:
                    finalInput,

                  top_k:
                    10,

                  mode:
                    "analysis",

                  active_document_ids:

                    activeDocuments.map(

                      doc =>

                        doc.document_id

                    )

                })

            }

          );

        if (
          !response.ok
        ) {

          throw new Error(

            `Request failed: ${response.status}`

          );

        }

        const data =
          await response.json();

        const assistantContent =

          data.analysis ||

          data.answer ||

          data.comparison ||

          "No response returned.";

        setMessages(

          prev => {

            const updated =
              [...prev];

            updated[
              updated.length - 1
            ] = {

              role:
                "assistant",

              content:
                assistantContent,

              citations:
                data.citations || [],

              evidence:
                data.evidence || {},

              noveltyAnalysis:
                data.novelty_analysis || null

            };

            return updated;

          }

        );

        // ============================
        // SOURCES
        // ============================

        setSources(

          data.citations ||

          data.related_theses ||

          []

        );

        // ============================
        // EVIDENCE
        // ============================

        setEvidence(

          data.evidence || {}

        );

        // ============================
        // MATRIX
        // ============================

        setEvidenceMatrix(

          data.evidence_matrix || {}

        );

        // ============================
        // GAP ANALYSIS
        // ============================

        setGapAnalysis(

          data.gap_analysis ||

          data.research_gaps ||

          {}

        );

      } catch (error) {

        console.error(
          "CHAT ERROR:",
          error
        );

        setMessages(

          prev => {

            const updated =
              [...prev];

            updated[
              updated.length - 1
            ] = {

              role:
                "assistant",

              content:

                `Terjadi error saat memproses request.\n\n${error.message}`

            };

            return updated;

          }

        );

      } finally {

        setLoading(false);

      }

    };

  // =====================================
  // ENTER
  // =====================================

  const handleKeyDown =
    (e) => {

      if (

        e.key === "Enter"

        &&

        !e.shiftKey

      ) {

        e.preventDefault();

        sendMessage();

      }

    };

  // =====================================
  // UI
  // =====================================

  return (

    <div className="chat-modern-shell">

      <div

        className={`modern-messages ${
          messages.length === 0
            ? "empty-chat"
            : ""
        }`}

      >

        {

          messages.length === 0

            ? (

              <ChatHero
                setInput={
                  setInput
                }
              />

            )

            : (

              messages.map(

                (
                  msg,
                  idx
                ) => (

                  <MessageBubble

                    key={
                      msg.id || idx
                    }

                    role={
                      msg.role
                    }

                    content={
                      msg.content
                    }

                    citations={
                      msg.citations
                    }

                    evidence={
                      msg.evidence
                    }

                    noveltyAnalysis={
                      msg.noveltyAnalysis
                    }

                    attachedDocuments={
                      msg.attachedDocuments
                    }

                    sources={
                      sources
                    }

                    setSelectedThesis={
                      setSelectedThesis
                    }

                    setActiveCitation={
                      setActiveCitation
                    }

                  />

                )

              )

            )

        }

        {

          loading && (

            <ThinkingIndicator />

          )

        }

      </div>

      <ChatInput

        input={input}

        setInput={
          setInput
        }

        sendMessage={
          sendMessage
        }

        loading={
          loading
        }

        handleFileUpload={
          handleFileUpload
        }

        handleKeyDown={
          handleKeyDown
        }

        activeDocuments={
          activeDocuments
        }

        uploadingDocuments={
          uploadingDocuments
        }

        removeDocument={
          removeDocument
        }

        clearDocuments={
          clearDocuments
        }

      />

    </div>

  );

}