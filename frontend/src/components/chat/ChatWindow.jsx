import {
  useState,
  useRef,
  useEffect
} from "react";

import { API_BASE_URL }
from "../../services/api";

import MessageBubble
from "./MessageBubble";

import ChatHero
from "./ChatHero";

import ChatInput
from "./ChatInput";

import ThinkingIndicator
from "./ThinkingIndicator";

import UploadStatus
from "./UploadStatus";

export default function ChatWindow({

  messages = [],

  setMessages,

  setSources,

  activeCitation,

  setActiveCitation

}) {

  const [input, setInput] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [uploadedFiles, setUploadedFiles] =
    useState([]);

  const [uploadingFiles, setUploadingFiles] =
    useState([]);

  const messagesEndRef =
    useRef(null);

  useEffect(() => {

    if (messages.length > 0) {

      messagesEndRef.current
        ?.scrollIntoView({

          behavior: "smooth"
        });

    }

  }, [messages, uploadingFiles]);

  // =====================================
  // DEBUG
  // =====================================

  console.log(
    "CHATWINDOW MESSAGES:",
    messages
  );

  console.log(
    "CHATWINDOW LENGTH:",
    messages.length
  );

  // =====================================
  // FILE UPLOAD
  // =====================================

  const handleFileUpload = async (e) => {

    const files = Array.from(
      e.target.files
    );

    if (!files.length) return;

    for (const file of files) {

      const uploadItem = {

        id:
          Date.now() + file.name,

        name:
          file.name,

        status:
          "Analyzing document..."
      };

      setUploadingFiles((prev) => [

        ...prev,

        uploadItem
      ]);

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

              method: "POST",

              body: formData
            }
          );

        if (!response.ok) {

          throw new Error(
            "Upload failed"
          );
        }

        const data =
          await response.json();

        setUploadingFiles((prev) =>

          prev.map((f) =>

            f.id === uploadItem.id

              ? {

                  ...f,

                  status:
                    "Indexed successfully"
                }

              : f
          )
        );

        setUploadedFiles((prev) => [

          ...prev,

          {

            name:
              file.name,

            chunks:
              data.chunks || 0,

            pages:
              data.pages || 0,

            type:
              data.file_type || "pdf"
          }
        ]);

        setTimeout(() => {

          setUploadingFiles((prev) =>

            prev.filter(

              (f) =>
                f.id !== uploadItem.id
            )
          );

        }, 1200);

      } catch (err) {

        console.error(err);

        setUploadingFiles((prev) =>

          prev.map((f) =>

            f.id === uploadItem.id

              ? {

                  ...f,

                  status:
                    "Upload failed"
                }

              : f
          )
        );
      }
    }
  };

  // =====================================
  // SEND MESSAGE
  // =====================================

  const sendMessage = async () => {

    if (!input.trim()) return;

    const finalInput = input;

    const userMessage = {

      role: "user",

      content: finalInput
    };

    setMessages((prev) => [

      ...prev,

      userMessage,

      {

        role: "assistant",

        content: ""
      }
    ]);

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

            method: "POST",

            headers: {

              "Content-Type":
                "application/json"
            },

            body: JSON.stringify({

              query:
                finalInput,

              top_k: 5,

              mode:
                "analysis"
            })
          }
        );

      if (!response.ok) {

        throw new Error(
          `Research request failed: ${response.status}`
        );
      }

      const data =
        await response.json();

      console.log(
        "FULL RESPONSE:",
        data
      );

      setMessages((prev) => {

        const updated =
          [...prev];

        updated[
          updated.length - 1
        ] = {

          role: "assistant",

          content:
            data.analysis ||
            "No analysis returned.",

          citations:
            data.citations || [],

          evidence:
            data.evidence || {}
        };

        return updated;
      });

      setSources(
        data.citations || []
      );

    } catch (error) {

      console.error(error);

      setMessages((prev) => {

        const updated =
          [...prev];

        updated[
          updated.length - 1
        ] = {

          role: "assistant",

          content:
            `Terjadi error saat memproses request.\n\n${error.message}`
        };

        return updated;
      });

    } finally {

      setLoading(false);
    }
  };

  // =====================================
  // ENTER KEY
  // =====================================

  const handleKeyDown = (e) => {

    if (

      e.key === "Enter" &&

      !e.shiftKey

    ) {

      e.preventDefault();

      sendMessage();
    }
  };

  // =====================================
  // RENDER DEBUG
  // =====================================

  console.log(
    "RENDERING CHAT",
    messages
  );

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

          messages.length === 0 ? (

            <ChatHero
              setInput={setInput}
            />

          ) : (

            messages.map(

              (msg, idx) => {

                console.log(
                  "MESSAGE",
                  idx,
                  msg
                );

                return (

                  <MessageBubble

                    key={idx}

                    role={msg.role}

                    content={msg.content}

                  />

                );
              }
            )

          )
        }

        <UploadStatus

          uploadingFiles={
            uploadingFiles
          }

        />

        {

          loading && (

            <ThinkingIndicator />
          )
        }

        <div ref={messagesEndRef} />

      </div>

      <ChatInput

        input={input}

        setInput={setInput}

        sendMessage={sendMessage}

        loading={loading}

        uploadedFiles={uploadedFiles}

        handleFileUpload={
          handleFileUpload
        }

        handleKeyDown={
          handleKeyDown
        }

      />

    </div>
  );
}