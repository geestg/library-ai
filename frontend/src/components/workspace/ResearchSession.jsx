import {
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react";

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
  // REFS
  // =====================================

  const messagesRef =
    useRef(null);

  const shouldAutoScrollRef =
    useRef(true);

  const previousMessageCountRef =
    useRef(messages.length);

  // =====================================
  // UI STATE
  // =====================================

  const [

    showScrollToLatest,

    setShowScrollToLatest,

  ] = useState(false);

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

    streamProgress,

    sendMessage,

    stopGeneration,

    handleKeyDown,

  } = useResearchSession({

    // =================================
    // SESSION
    // =================================

    sessionId,

    // =================================
    // ACTIVE DOCUMENTS
    // =================================

    activeDocuments,

    // =================================
    // CONVERSATION
    // =================================

    setMessages,

    // =================================
    // SOURCES
    // =================================

    setSources,

    // =================================
    // EVIDENCE
    // =================================

    setEvidence,

    setEvidenceMatrix,

    setGapAnalysis,

    // =================================
    // RESEARCH PROFILE
    // =================================

    setResearchProfile,

    // =================================
    // UI
    // =================================

    setActiveCitation,

  });

  // =====================================
  // SCROLL TO LATEST
  // =====================================

  const scrollToLatest =
    useCallback((

      behavior = "smooth"

    ) => {

      const container =
        messagesRef.current;

      if (!container) {

        return;

      }

      container.scrollTo({

        top:
          container.scrollHeight,

        behavior,

      });

      shouldAutoScrollRef.current =
        true;

      setShowScrollToLatest(
        false
      );

    }, []);

  // =====================================
  // DETECT USER SCROLL
  // =====================================

  const handleConversationScroll =
    useCallback(() => {

      const container =
        messagesRef.current;

      if (!container) {

        return;

      }

      const distanceFromBottom =

        container.scrollHeight

        -

        container.scrollTop

        -

        container.clientHeight;

      const isNearBottom =

        distanceFromBottom <= 120;

      shouldAutoScrollRef.current =

        isNearBottom;

      setShowScrollToLatest(

        !isNearBottom

      );

    }, []);

  // =====================================
  // DETECT NEW CONVERSATION TURN
  // =====================================

  useEffect(() => {

    const currentMessageCount =
      messages.length;

    const previousMessageCount =
      previousMessageCountRef.current;

    if (

      currentMessageCount >

      previousMessageCount

    ) {

      const latestMessage =

        messages[
          currentMessageCount - 1
        ];

      if (

        latestMessage?.role ===
        "user"

      ) {

        shouldAutoScrollRef.current =
          true;

        setShowScrollToLatest(
          false
        );

      }

    }

    previousMessageCountRef.current =

      currentMessageCount;

  }, [

    messages,

  ]);

  // =====================================
  // AUTO SCROLL DURING STREAM
  // =====================================

  useEffect(() => {

    if (

      !shouldAutoScrollRef.current

    ) {

      return;

    }

    const frame =

      requestAnimationFrame(() => {

        const container =
          messagesRef.current;

        if (!container) {

          return;

        }

        container.scrollTo({

          top:
            container.scrollHeight,

          behavior:
            "auto",

        });

      });

    return () => {

      cancelAnimationFrame(
        frame
      );

    };

  }, [

    messages,

    conversationState,

    streamProgress,

  ]);

  // =====================================
  // SESSION CHANGE
  // =====================================

  useEffect(() => {

    shouldAutoScrollRef.current =
      true;

    previousMessageCountRef.current =
      messages.length;

    setShowScrollToLatest(
      false
    );

    const frame =

      requestAnimationFrame(() => {

        const container =
          messagesRef.current;

        if (!container) {

          return;

        }

        container.scrollTop =
          container.scrollHeight;

      });

    return () => {

      cancelAnimationFrame(
        frame
      );

    };

  }, [

    sessionId,

  ]);

  // =====================================
  // UI
  // =====================================

  return (

    <div className="research-session">

      {/* ================================= */}
      {/* CONVERSATION */}
      {/* ================================= */}

      <SessionConversation

        ref={messagesRef}

        messages={messages}

        conversationState={
          conversationState
        }

        streamProgress={
          streamProgress
        }

        sources={sources}

        setInput={setInput}

        setSelectedThesis={
          setSelectedThesis
        }

        setActiveCitation={
          setActiveCitation
        }

        onScroll={
          handleConversationScroll
        }

        showScrollToLatest={
          showScrollToLatest
        }

        onScrollToLatest={() =>

          scrollToLatest(
            "smooth"
          )

        }

      />

      {/* ================================= */}
      {/* CHAT INPUT */}
      {/* ================================= */}

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