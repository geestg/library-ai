import {
  useState,
  useEffect
} from "react";

import {
  API_BASE_URL
} from "../../services/api";

import MessageBubble
from "./MessageBubble";

import ChatHero
from "./ChatHero";

import ChatInput
from "./ChatInput";

import ThinkingIndicator
from "./ThinkingIndicator";

export default function ChatWindow({

  messages = [],

  setMessages,

  setSources,

  setEvidence,

  activeCitation,

  setActiveCitation

}) {

  // =====================================
  // CHAT STATE
  // =====================================

  const [input, setInput] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  // =====================================
  // ACTIVE DOCUMENT
  // =====================================

  const [activeDocument, setActiveDocument] =
    useState(null);

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
  // CLEAR DOCUMENT
  // =====================================

  const clearDocument = () => {

    setActiveDocument(
      null
    );

  };

  // =====================================
  // FILE UPLOAD
  // =====================================

  const handleFileUpload =
    async (e) => {

      const files =
        Array.from(
          e.target.files
        );

      if (!files.length) {
        return;
      }

      for (const file of files) {

        setActiveDocument({

          filename:
            file.name,

          status:
            "processing"

        });

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
              "Upload failed"
            );

          }

          const data =
            await response.json();

          if (
            data.document_id
          ) {

            setActiveDocument({

              document_id:
                data.document_id,

              filename:
                data.filename,

              pages:
                data.pages || 0,

              chunks:
                data.chunks || 0,

              status:
                "ready"

            });

          }

        } catch (error) {

          console.error(
            error
          );

          setActiveDocument({

            filename:
              file.name,

            status:
              "error"

          });

        }

      }

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
        input;

      setMessages(
        (prev) => [

          ...prev,

          {

            role:
              "user",

            content:
              finalInput,

            attachedDocument:
              activeDocument

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

      setLoading(
        true
      );

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
                    5,

                  mode:
                    "analysis",

                  active_document_id:

                    activeDocument?.document_id ||

                    null

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

        setMessages(
          (prev) => {

            const updated =
              [...prev];

            updated[
              updated.length - 1
            ] = {

              role:
                "assistant",

              content:

                data.answer ||

                data.analysis ||

                "No response returned.",

              citations:
                data.citations || [],

              evidence:
                data.evidence || {}

            };

            return updated;

          }

        );

        setSources(
          data.citations || []
        );

        setEvidence(
          data.evidence || {}
        );

        // =================================
        // AUTO RELEASE DOCUMENT
        // =================================

        if (
          activeDocument
        ) {

          setTimeout(
            () => {

              setActiveDocument(
                null
              );

            },
            1000
          );

        }

      } catch (error) {

        console.error(
          error
        );

        setMessages(
          (prev) => {

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

        setLoading(
          false
        );

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

                    attachedDocument={
                      msg.attachedDocument
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

        activeDocument={
          activeDocument
        }

        clearDocument={
          clearDocument
        }

      />

    </div>

  );

}