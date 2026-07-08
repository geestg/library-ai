import {

  useCallback,

  useEffect,

  useRef,

  useState,

} from "react";

import {

  ArrowDown,

} from "lucide-react";

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

  // =====================================
  // UI STATE
  // =====================================

  const [

    showScrollButton,

    setShowScrollButton,

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
  // SCROLL TO BOTTOM
  // =====================================

  const scrollToBottom =
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

      setShowScrollButton(
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

        distanceFromBottom < 120;

      shouldAutoScrollRef.current =

        isNearBottom;

      setShowScrollButton(

        !isNearBottom

      );

    }, []);

  // =====================================
  // AUTO SCROLL
  // =====================================

  useEffect(() => {

    if (

      !shouldAutoScrollRef.current

    ) {

      return;

    }

    const frame =

      requestAnimationFrame(() => {

        scrollToBottom(
          "smooth"
        );

      });

    return () => {

      cancelAnimationFrame(
        frame
      );

    };

  }, [

    messages,

    conversationState,

    scrollToBottom,

  ]);

  // =====================================
  // NEW USER MESSAGE
  // =====================================

  useEffect(() => {

    shouldAutoScrollRef.current =
      true;

  }, [

    messages.length,

  ]);

  // =====================================
  // UI
  // =====================================

  return (

    <div className="research-session">

      <div className="conversation-shell">

        <SessionConversation

          ref={messagesRef}

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

          onScroll={
            handleConversationScroll
          }

        />

        {

          showScrollButton && (

            <button

              type="button"

              className="scroll-to-latest"

              onClick={() =>

                scrollToBottom(
                  "smooth"
                )

              }

              aria-label="Scroll to latest message"

            >

              <ArrowDown

                size={17}

              />

              <span>

                Latest

              </span>

            </button>

          )

        }

      </div>

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