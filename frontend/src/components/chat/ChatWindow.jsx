import { useEffect, useState } from "react";
import { API_BASE_URL } from "../../services/api";
import MessageBubble from "./MessageBubble";
import ChatHero from "./ChatHero";
import ChatInput from "./ChatInput";
import ThinkingIndicator from "./ThinkingIndicator";
import ImagePreviewModal from "../ImagePreviewModal";

export default function ChatWindow({
  userRole = "student",
  sessionId = "chat_session",
  messages = [],
  setMessages,
  setSources,
  setEvidence,
  activeCitation,
  setActiveCitation,
  selectedThesis,
  setSelectedThesis,
  activeDocument,
  setActiveDocument,
  onMessageSent,
}) {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [activeDocuments, setActiveDocuments] = useState([]);
  const [uploadingDocuments, setUploadingDocuments] = useState([]);
  const [previewImage, setPreviewImage] = useState(null);

  useEffect(() => {
    const container = document.querySelector(".modern-messages");
    if (!container) return;
    container.scrollTo({ top: container.scrollHeight, behavior: "smooth" });
  }, [messages, loading]);

  useEffect(() => {
    if (messages && messages.length > 0) {
      const lastAsst = [...messages].reverse().find((m) => m.role === "assistant");
      if (lastAsst && (lastAsst.sources?.length > 0 || lastAsst.citations?.length > 0)) {
        setSources(lastAsst.sources || lastAsst.citations);
      }
    }
  }, [messages, setSources]);

  const removeDocument = (documentId) => {
    setActiveDocuments((prev) => prev.filter((doc) => doc.document_id !== documentId));
  };

  const removeSelectedFile = (index) => {
    setSelectedFiles((prev) => {
      const file = prev[index];
      if (file?.previewUrl?.startsWith("blob:")) {
        URL.revokeObjectURL(file.previewUrl);
      }
      return prev.filter((_, i) => i !== index);
    });
  };

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files || []);
    if (!files.length) return;

    const newFiles = files.map((file) => ({
      id: `${Date.now()}-${file.name}`,
      name: file.name,
      type: file.type,
      size: file.size,
      file,
      previewUrl: file.type.startsWith("image/") ? URL.createObjectURL(file) : null,
    }));

    setSelectedFiles((prev) => [...prev, ...newFiles]);
    e.target.value = "";
  };

  const fileToDataUrl = (file) =>
    new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = () => reject(new Error(`Failed to read image ${file.name}`));
      reader.readAsDataURL(file.file);
    });

  const uploadPdfFile = async (file) => {
    const formData = new FormData();
    formData.append("file", file.file);
    formData.append("session_id", sessionId);

    const uploadRes = await fetch(API_BASE_URL + "/upload-pdf", {
      method: "POST",
      body: formData,
    });

    if (!uploadRes.ok) {
      const t = await uploadRes.text().catch(() => "");
      throw new Error(`Upload document failed: ${uploadRes.status} ${t}`);
    }

    const uploadData = await uploadRes.json();

    if (uploadData.status !== "success") {
      throw new Error(uploadData.message || "Document upload failed");
    }

    return uploadData;
  };

  const sendMessage = async () => {
    if (!input.trim() && selectedFiles.length === 0) return;

    const userMessage = input.trim();
    const currentSelectedFiles = [...selectedFiles];

    setInput("");
    setSelectedFiles([]);
    setLoading(true);

    const userMsgObj = {
      id: `${Date.now()}-user`,
      role: "user",
      content: userMessage,
      attachments: currentSelectedFiles,
      attachedDocuments: [...activeDocuments],
    };

    setMessages((prev) => [...prev, userMsgObj]);

    try {
      const imageFiles = currentSelectedFiles.filter((f) => f.type.startsWith("image/"));
      const pdfFiles = currentSelectedFiles.filter((f) => !f.type.startsWith("image/"));

      const imagePayloads = [];
      for (const img of imageFiles) {
        const dataUrl = await fileToDataUrl(img);
        imagePayloads.push({ name: img.name, dataUrl });
      }

      const uploadedDocuments = [];
      if (pdfFiles.length > 0) {
        setUploadingDocuments(pdfFiles.map((f) => f.name));
        for (const pdf of pdfFiles) {
          const docData = await uploadPdfFile(pdf);
          const newDoc = {
            document_id: docData.document_id,
            filename: docData.filename,
            pages: docData.pages,
            preview: docData.preview,
          };
          uploadedDocuments.push(newDoc);
          setActiveDocuments((prev) => [...prev, newDoc]);
        }
        setUploadingDocuments([]);
      }

      const currentDocuments = [...activeDocuments, ...uploadedDocuments];

      if (imagePayloads.length > 0) {
        const firstImage = imagePayloads[0];

        const visionRes = await fetch(API_BASE_URL + "/api/vision/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json", "X-User-Role": userRole },
          body: JSON.stringify({
            prompt: userMessage,
            image_base64: firstImage.dataUrl,
            session_id: sessionId,
          }),
        });

        if (!visionRes.ok) {
          const t = await visionRes.text().catch(() => "");
          throw new Error(`Vision request failed: ${visionRes.status} ${t}`);
        }

        const visionData = await visionRes.json();
        const content = visionData.response || visionData.answer || visionData.analysis || "No response returned.";

        setMessages((prev) => {
          return [
            ...prev,
            {
              id: `${Date.now()}-assistant`,
              role: "assistant",
              content,
              citations: visionData.citations || [],
              sources: visionData.sources || [],
            },
          ];
        });

        setSources(visionData.sources || visionData.citations || []);
        onMessageSent?.();
        return;
      }

      if (currentDocuments.length > 0) {
        const targetDocument = currentDocuments[currentDocuments.length - 1];

        const documentResponse = await fetch(API_BASE_URL + "/document/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json", "X-User-Role": userRole },
          body: JSON.stringify({
            session_id: sessionId,
            document_id: targetDocument.document_id,
            question: userMessage,
          }),
        });

        if (!documentResponse.ok) {
          const t = await documentResponse.text().catch(() => "");
          throw new Error(`Document request failed: ${documentResponse.status} ${t}`);
        }

        const documentData = await documentResponse.json();
        const content = documentData.response || documentData.answer || "No response returned.";

        setMessages((prev) => {
          return [
            ...prev,
            {
              id: `${Date.now()}-assistant`,
              role: "assistant",
              content,
              citations: documentData.citations || [],
              sources: documentData.sources || [],
            },
          ];
        });

        setSources(documentData.sources || documentData.citations || []);
        if (documentData.evidence && setEvidence) {
          setEvidence(documentData.evidence);
        }
        onMessageSent?.();
        return;
      }

      const res = await fetch(API_BASE_URL + "/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-User-Role": userRole },
        body: JSON.stringify({
          message: userMessage,
          query: userMessage,
          session_id: sessionId,
        }),
      });

      if (!res.ok) {
        const t = await res.text().catch(() => "");
        throw new Error(`Chat request failed: ${res.status} ${t}`);
      }

      const resData = await res.json();
      const content = resData.response || resData.answer || resData.result || "No response returned.";

      setMessages((prev) => {
        return [
          ...prev,
          {
            id: `${Date.now()}-assistant`,
            role: "assistant",
            content,
            citations: resData.citations || [],
            sources: resData.sources || [],
            data: resData.data || null,
          },
        ];
      });

      setSources(resData.sources || resData.citations || []);
      if (resData.evidence && setEvidence) {
        setEvidence(resData.evidence);
      }
      onMessageSent?.();
    } catch (err) {
      console.error("Failed to send message:", err);
      setMessages((prev) => [
        ...prev,
        {
          id: `${Date.now()}-error`,
          role: "assistant",
          content: `⚠️ Terjadi kendala koneksi server: ${err.message}. Silakan coba lagi.`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const activateMessageSources = (msg) => {
    let targetSources = msg?.sources?.length > 0 ? msg.sources : msg?.citations;
    if (!targetSources || targetSources.length === 0) {
      for (const m of [...messages].reverse()) {
        if (m.role === "assistant" && (m.sources?.length > 0 || m.citations?.length > 0)) {
          targetSources = m.sources?.length > 0 ? m.sources : m.citations;
          break;
        }
      }
    }
    if (targetSources && targetSources.length > 0) {
      setSources(targetSources);
    }
  };

  const inputComponent = (
    <ChatInput
      input={input}
      setInput={setInput}
      sendMessage={sendMessage}
      loading={loading}
      handleFileSelect={handleFileSelect}
      handleKeyDown={handleKeyDown}
      activeDocuments={activeDocuments}
      selectedFiles={selectedFiles}
      removeSelectedFile={removeSelectedFile}
      uploadingDocuments={uploadingDocuments}
      removeDocument={removeDocument}
    />
  );

  return (
    <div className="modern-chat-container">
      {/* ============================= */}


      {/* ============================= */}
      {/* MESSAGES LIST AREA */}
      {/* ============================= */}
      <div className={`modern-messages ${messages.length === 0 ? "empty-chat" : ""}`}>
        {messages.length === 0 ? (
          <div className="empty-chat-container">
            <ChatHero />
            <div className="empty-chat-input-box">
              {inputComponent}
            </div>
          </div>
        ) : (
          messages.map((msg) => (
            <MessageBubble
              key={msg.id}
              role={msg.role}
              content={msg.content}
              citations={msg.citations}
              sources={msg.sources}
              attachedDocuments={msg.attachedDocuments}
              attachments={msg.attachments}
              data={msg.data}
              onImageClick={(img) => setPreviewImage(img)}
              setActiveCitation={setActiveCitation}
              setSelectedThesis={setSelectedThesis}
              onActivateMessageSources={() => activateMessageSources(msg)}
            />
          ))
        )}

        {loading && <ThinkingIndicator />}
      </div>

      {/* ============================= */}
      {/* FLOATING CAPSULE INPUT (AFTER FIRST MESSAGE) */}
      {/* ============================= */}
      {messages.length > 0 && inputComponent}

      {/* ============================= */}
      {/* IMAGE PREVIEW MODAL */}
      {/* ============================= */}
      {previewImage && (
        <ImagePreviewModal
          imageUrl={previewImage.url}
          imageName={previewImage.name}
          onClose={() => setPreviewImage(null)}
        />
      )}
    </div>
  );
}