import { useEffect, useState } from "react";
import { API_BASE_URL } from "../../services/api";
import MessageBubble from "./MessageBubble";
import ChatHero from "./ChatHero";
import ChatInput from "./ChatInput";
import ThinkingIndicator from "./ThinkingIndicator";
import ImagePreviewModal from "../ImagePreviewModal";

export default function ChatWindow({
  messages = [],
  setMessages,
  setSources,
  setEvidence,
  activeCitation,
  setActiveCitation,
  activeDocument,
  setActiveDocument,
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

    const filesToSend = [...selectedFiles];
    const attachments = filesToSend.map((file) => ({
      id: file.id,
      name: file.name,
      type: file.type,
      previewUrl: file.previewUrl,
      isImage: file.type.startsWith("image/"),
    }));

    const userMessage = {
      id: `${Date.now()}-user`,
      role: "user",
      content: input,
      attachedDocuments: activeDocuments,
      attachments,
    };

    setMessages((prev) => [...prev, userMessage]);

    const finalInput = input;
    setInput("");
    setSelectedFiles([]);

    const textarea = document.querySelector(".floating-input textarea");
    if (textarea) textarea.style.height = "auto";

    setLoading(true);
    setUploadingDocuments([]);

    try {
      const imageFiles = filesToSend.filter((file) => file.type?.startsWith("image/"));
      const pdfFiles = filesToSend.filter((file) => {
        const lowerName = (file.name || "").toLowerCase();
        return file.type === "application/pdf" || lowerName.endsWith(".pdf");
      });

      const uploadedDocuments = [];
      const imagePayloads = [];

      if (pdfFiles.length > 0) {
        setUploadingDocuments(pdfFiles.map((file) => ({ id: file.id, filename: file.name })));

        for (const file of pdfFiles) {
          const uploadData = await uploadPdfFile(file);
          uploadedDocuments.push({
            document_id: uploadData.document_id,
            filename: uploadData.filename,
            file_type: uploadData.file_type,
            pages: uploadData.pages,
            chunks: uploadData.chunks,
          });
        }

        setActiveDocuments((prev) => {
          const next = [...prev];
          const existingIds = new Set(prev.map((doc) => doc.document_id));

          for (const document of uploadedDocuments) {
            if (!existingIds.has(document.document_id)) {
              next.push(document);
            }
          }

          return next;
        });
      }

      if (imageFiles.length > 0) {
        setUploadingDocuments(imageFiles.map((file) => ({ id: file.id, filename: file.name })));

        for (const file of imageFiles) {
          imagePayloads.push({
            id: file.id,
            name: file.name,
            dataUrl: await fileToDataUrl(file),
          });
        }
      }

      const currentDocuments = [...activeDocuments, ...uploadedDocuments];

      if (imagePayloads.length > 0) {
        const firstImage = imagePayloads[0];

        const visionRes = await fetch(API_BASE_URL + "/api/vision/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            prompt: finalInput,
            image_base64: firstImage.dataUrl,
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
        return;
      }

      if (currentDocuments.length > 0) {
        const targetDocument = currentDocuments[currentDocuments.length - 1];

        const documentResponse = await fetch(API_BASE_URL + "/document/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            document_id: targetDocument.document_id,
            question: finalInput,
          }),
        });

        if (!documentResponse.ok) {
          const t = await documentResponse.text().catch(() => "");
          throw new Error(`Document request failed: ${documentResponse.status} ${t}`);
        }

        const data = await documentResponse.json();
        const content = data.answer || data.response || data.analysis || "No response returned.";

        setMessages((prev) => {
          return [
            ...prev,
            {
              id: `${Date.now()}-assistant`,
            role: "assistant",
            content,
            citations: data.citations || [],
            sources: data.sources || [],
            },
          ];
        });

        setSources(data.sources || data.citations || []);
        return;
      }

      const chatResponse = await fetch(API_BASE_URL + "/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: finalInput }),
      });

      if (!chatResponse.ok) throw new Error("Request failed: " + chatResponse.status);

      const data = await chatResponse.json();
      const content = data.response || data.answer || data.analysis || "No response returned.";

      setMessages((prev) => {
        return [
          ...prev,
          {
            id: `${Date.now()}-assistant`,
          role: "assistant",
          content,
          citations: data.citations || [],
          sources: data.sources || [],
          },
        ];
      });

      setSources(data.sources || data.citations || []);
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => {
        return [
          ...prev,
          {
            id: `${Date.now()}-assistant-error`,
          role: "assistant",
          content: "Error: " + error.message,
          },
        ];
      });
    } finally {
      setUploadingDocuments([]);
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chat-modern-shell">
      {previewImage && <ImagePreviewModal image={previewImage} onClose={() => setPreviewImage(null)} />}

      <div className={`modern-messages ${messages.length === 0 ? "empty-chat" : ""}`}>
        {messages.length === 0 ? (
          <ChatHero setInput={setInput} />
        ) : (
          messages.map((msg, idx) => (
            <MessageBubble
              key={msg.id || idx}
              role={msg.role}
              content={msg.content}
              citations={msg.citations}
              evidence={msg.evidence}
              attachedDocuments={msg.attachedDocuments}
              attachments={msg.attachments}
              onImageClick={setPreviewImage}
              setActiveCitation={setActiveCitation}
            />
          ))
        )}

        {loading && <ThinkingIndicator />}
      </div>

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
    </div>
  );
}