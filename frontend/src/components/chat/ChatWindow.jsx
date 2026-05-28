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

  // =====================================
  // STATE
  // =====================================

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

  // =====================================
  // AUTO SCROLL
  // =====================================

  useEffect(() => {

    if (messages.length > 0) {  

    messagesEndRef.current
      ?.scrollIntoView({

        behavior: "smooth"
      });

    }
    
  }, [messages, uploadingFiles]);

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

        name: file.name,

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

        // ===============================
        // UPDATE STATUS
        // ===============================

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

        // ===============================
        // SAVE FILE
        // ===============================

        setUploadedFiles((prev) => [

          ...prev,

          {

            name: file.name,

            chunks:
              data.chunks || 0,

            pages:
              data.pages || 0,

            type:
              data.file_type || "pdf"
          }
        ]);

        // ===============================
        // REMOVE STATUS
        // ===============================

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

    // ===================================
    // FILE CONTEXT
    // ===================================

    let fileContext = "";

    if (uploadedFiles.length > 0) {

      fileContext = `

Attached academic documents:
${uploadedFiles
  .map((f) => `- ${f.name}`)
  .join("\n")}
`;
    }

    // ===================================
    // USER MESSAGE
    // ===================================

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

    // ===================================
    // RESET INPUT
    // ===================================

    setInput("");

    // ===================================
    // RESET TEXTAREA HEIGHT
    // ===================================

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

          `${API_BASE_URL}/chat-stream`,

          {

            method: "POST",

            headers: {

              "Content-Type":
                "application/json"
            },

            body: JSON.stringify({

              message:
                finalInput + fileContext
            })
          }
        );

      if (!response.body) {

        throw new Error(
          "Streaming unavailable"
        );
      }

      const reader =
        response.body.getReader();

      const decoder =
        new TextDecoder();

      let streamedText = "";

      let buffer = "";

      while (true) {

        const {

          done,

          value

        } = await reader.read();

        if (done) break;

        buffer +=
          decoder.decode(value);

        const lines =
          buffer.split("\n");

        buffer =
          lines.pop() || "";

        for (const line of lines) {

          if (!line.trim())
            continue;

          try {

            const parsed =
              JSON.parse(line);

            // =========================
            // TOKEN
            // =========================

            if (
              parsed.type === "token"
            ) {

              streamedText +=
                parsed.content;

              setMessages((prev) => {

                const updated =
                  [...prev];

                updated[
                  updated.length - 1
                ] = {

                  role: "assistant",

                  content:
                    streamedText
                };

                return updated;
              });
            }

            // =========================
            // SOURCES
            // =========================

            if (
              parsed.type === "sources"
            ) {

              setSources(
                parsed.data || []
              );
            }

            // =========================
            // CITATIONS
            // =========================

            if (
              parsed.type === "citations"
            ) {

              console.log(
                "citations",
                parsed.data
              );
            }

          } catch (err) {

            console.error(
              "Stream parse error:",
              err
            );
          }
        }
      }

    } catch (error) {

      console.error(error);

      setMessages((prev) => [

        ...prev,

        {

          role: "assistant",

          content:
            "Terjadi error saat memproses request."
        }
      ]);

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
  // UI
  // =====================================

  return (

    <div className="chat-modern-shell">

      {/* ============================= */}
      {/* CHAT AREA */}
      {/* ============================= */}

      <div className="modern-messages">

        {

          messages.length === 0 ? (

            <ChatHero
              setInput={setInput}
            />

          ) : (

            <>

              {

                messages.map(
                  (msg, idx) => (

                    <MessageBubble

                      key={idx}

                      role={msg.role}

                      content={msg.content}

                      setActiveCitation={
                        setActiveCitation
                      }

                    />

                  )
                )
              }

            </>

          )
        }

        {/* ========================= */}
        {/* UPLOAD STATUS */}
        {/* ========================= */}

        <UploadStatus

          uploadingFiles={
            uploadingFiles
          }

        />

        {/* ========================= */}
        {/* THINKING */}
        {/* ========================= */}

        {

          loading && (

            <ThinkingIndicator />

          )
        }

        <div ref={messagesEndRef} />

      </div>

      {/* ============================= */}
      {/* INPUT */}
      {/* ============================= */}

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