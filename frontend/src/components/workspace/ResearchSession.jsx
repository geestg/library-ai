import { useEffect } from "react";

import SessionConversation from "./SessionConversation";

import ChatInput from "../chat/ChatInput";

import useResearchSession from "../../hooks/useResearchSession";
import useDocumentUpload from "../../hooks/useDocumentUpload";

export default function ResearchSession({

  // =====================================
  // SESSION
  // =====================================

  sessionId,

  // =====================================
  // CONVERSATION
  // =====================================

  messages = [],

  setMessages,

  // =====================================
  // SOURCES
  // =====================================

  sources = [],

  setSources,

  // =====================================
  // EVIDENCE
  // =====================================

  setEvidence,

  setEvidenceMatrix,

  setGapAnalysis,

  // =====================================
  // RESEARCH PROFILE
  // =====================================

  researchProfile,

  setResearchProfile,

  // =====================================
  // UI
  // =====================================

  activeCitation,

  setActiveCitation,

  setSelectedThesis,

}) {

  // =====================================
  // DOCUMENT HOOK
  // =====================================

  const {

    activeDocuments,

    uploadingDocuments,

    documentError,

    handleFileUpload,

    removeDocument,

    clearDocumentError,

    isDocumentDeleting,

  } = useDocumentUpload({

    sessionId,

  });

  // =====================================
  // RESEARCH HOOK
  // =====================================

  const {

    input,

    setInput,

    conversationState,

    sendMessage,

    stopGeneration,

    handleKeyDown,

  } = useResearchSession({

    sessionId,

    activeDocuments,

    setMessages,

    setSources,

    setEvidence,

    setEvidenceMatrix,

    setGapAnalysis,

    setResearchProfile,

    setActiveCitation,

  });

  // =====================================
  // AUTO SCROLL
  // =====================================

  useEffect(() => {

    const container = document.querySelector(
      ".modern-messages"
    );

    if (!container) {

      return;

    }

    container.scrollTo({

      top: container.scrollHeight,

      behavior: "smooth",

    });

  }, [

    messages,

    conversationState,

  ]);

  // =====================================
  // UI
  // =====================================

  return (

    <div className="research-session">

      <SessionConversation

        messages={messages}

        conversationState={
          conversationState
        }

        sources={sources}

        setInput={setInput}

        setSelectedThesis={
          setSelectedThesis
        }

        setActiveCitation={
          setActiveCitation
        }

      />

      <ChatInput

        input={input}

        setInput={setInput}

        sendMessage={sendMessage}

        stopGeneration={
          stopGeneration
        }

        conversationState={
          conversationState
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

        documentError={
          documentError
        }

        removeDocument={
          removeDocument
        }

        clearDocumentError={
          clearDocumentError
        }

        isDocumentDeleting={
          isDocumentDeleting
        }

      />

    </div>

  );

}