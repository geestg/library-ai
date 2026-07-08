import {
  useState,
  useCallback,
  useRef,
} from "react";

import useConversationState, {
  ConversationState,
} from "./useConversationState";

import useAssistantMessage from "./useAssistantMessage";
import useWorkspaceUpdater from "./useWorkspaceUpdater";
import useStreamingChat from "./useStreamingChat";

export default function useResearchSession({

  // =====================================
  // SESSION
  // =====================================

  sessionId,

  // =====================================
  // ACTIVE DOCUMENTS
  // =====================================

  activeDocuments = [],

  // =====================================
  // DOCUMENT CONSUMPTION
  // =====================================

  onDocumentsConsumed,

  // =====================================
  // CONVERSATION
  // =====================================

  setMessages,

  // =====================================
  // SOURCES
  // =====================================

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

  setResearchProfile,

  // =====================================
  // UI
  // =====================================

  setActiveCitation,

}) {

  // =====================================
  // INPUT
  // =====================================

  const [

    input,

    setInput,

  ] = useState("");

  // =====================================
  // INTERNAL
  // =====================================

  const sendingRef =
    useRef(false);

  // =====================================
  // CONVERSATION
  // =====================================

  const {

    conversationState,

    setThinking,

    setStreaming,

    setCompleted,

    setCancelled,

    setError,

    reset,

  } = useConversationState();

  // =====================================
  // ASSISTANT
  // =====================================

  const {

    appendConversation,

    appendToken,

    patchAssistant,

  } = useAssistantMessage({

    setMessages,

  });

  // =====================================
  // WORKSPACE
  // =====================================

  const {

    clearSelection,

    updateWorkspace,

  } = useWorkspaceUpdater({

    setSources,

    setEvidence,

    setEvidenceMatrix,

    setGapAnalysis,

    setResearchProfile,

    setActiveCitation,

  });

  // =====================================
  // STREAM
  // =====================================

  const {

    startStream,

    stopStream,

  } = useStreamingChat();

  // =====================================
  // SEND MESSAGE
  // =====================================

  const sendMessage =
    useCallback(async () => {

      // =================================
      // PREPARE INPUT
      // =================================

      const finalInput =
        input.trim();

      if (!finalInput) {

        return;

      }

      // =================================
      // DUPLICATE SEND GUARD
      // =================================

      if (sendingRef.current) {

        return;

      }

      // =================================
      // SNAPSHOT ACTIVE DOCUMENTS
      // =================================

      const documentsForMessage =

        activeDocuments.map(

          document => ({

            ...document,

          })

        );

      // =================================
      // BUILD ACTIVE DOCUMENT IDS
      // =================================

      const activeDocumentIds =

        documentsForMessage

          .map(

            document =>

              document.document_id

          )

          .filter(Boolean);

      // =================================
      // LOCK SEND
      // =================================

      sendingRef.current =
        true;

      // =================================
      // RESET CONVERSATION STATE
      // =================================

      reset();

      setThinking();

      clearSelection();

      // =================================
      // APPEND USER + ASSISTANT MESSAGE
      // =================================

      appendConversation(

        finalInput,

        documentsForMessage

      );

      // =================================
      // CLEAR TEXT INPUT
      // =================================

      setInput("");

      // =================================
      // SEND MESSAGE DEBUG
      // =================================

      console.log(

        "[SEND MESSAGE DEBUG]",

        {

          sessionId,

          finalInput,

          totalActiveDocuments:
            documentsForMessage.length,

          documentsForMessage,

          activeDocumentIds,

        }

      );

      try {

        await startStream({

          // =============================
          // SESSION
          // =============================

          sessionId,

          // =============================
          // QUERY
          // =============================

          query:
            finalInput,

          // =============================
          // DOCUMENTS
          // =============================

          activeDocumentIds,

          // =============================
          // STREAM START
          // =============================

          onStart() {

            setThinking();

          },

          // =============================
          // METADATA
          // =============================

          onMetadata(metadata) {

            console.info(

              "[STREAM]",

              metadata

            );

          },

          // =============================
          // TOKEN
          // =============================

          onToken(token) {

            if (

              conversationState !==

              ConversationState.STREAMING

            ) {

              setStreaming();

            }

            appendToken(

              token

            );

          },

          // =============================
          // CONTEXT
          // =============================

          onContext(context) {

            updateWorkspace(

              context

            );

          },

          // =============================
          // STREAM END
          // =============================

          onEnd() {

            // ===========================
            // UNLOCK SEND
            // ===========================

            sendingRef.current =
              false;

            // ===========================
            // COMPLETE CONVERSATION
            // ===========================

            setCompleted();

            // ===========================
            // CONSUME USED DOCUMENTS
            // ===========================

            if (

              documentsForMessage.length > 0

            ) {

              onDocumentsConsumed?.();

            }

          },

          // =============================
          // STREAM ERROR
          // =============================

          onError(error) {

            console.error(

              "[STREAM]",

              error

            );

            patchAssistant({

              content:

                "Terjadi error saat memproses request.",

            });

            // ===========================
            // KEEP DOCUMENTS FOR RETRY
            // ===========================

            sendingRef.current =
              false;

            setError();

          },

        });

      }

      catch (error) {

        // =================================
        // STOP GENERATION
        // =================================

        if (

          error?.name ===

          "AbortError"

        ) {

          // ===============================
          // KEEP DOCUMENTS FOR RETRY
          // ===============================

          sendingRef.current =
            false;

          setCancelled();

          return;

        }

        // =================================
        // GENERAL ERROR
        // =================================

        console.error(

          "[ResearchSession]",

          error

        );

        patchAssistant({

          content:

            `Terjadi error saat memproses request.\n\n${error.message}`,

        });

        // =================================
        // KEEP DOCUMENTS FOR RETRY
        // =================================

        sendingRef.current =
          false;

        setError();

      }

    }, [

      sessionId,

      input,

      conversationState,

      activeDocuments,

      onDocumentsConsumed,

      reset,

      setThinking,

      setStreaming,

      setCompleted,

      setCancelled,

      setError,

      clearSelection,

      appendConversation,

      appendToken,

      patchAssistant,

      updateWorkspace,

      startStream,

    ]);

  // =====================================
  // STOP GENERATION
  // =====================================

  const stopGeneration =
    useCallback(() => {

      if (

        !sendingRef.current

      ) {

        return;

      }

      stopStream();

      sendingRef.current =
        false;

      setCancelled();

    }, [

      stopStream,

      setCancelled,

    ]);

  // =====================================
  // HANDLE ENTER
  // =====================================

  const handleKeyDown =
    useCallback(

      (event) => {

        if (

          event.key !== "Enter"

        ) {

          return;

        }

        if (

          event.shiftKey

        ) {

          return;

        }

        event.preventDefault();

        if (

          sendingRef.current

        ) {

          return;

        }

        sendMessage();

      },

      [

        sendMessage,

      ]

    );

  // =====================================
  // PUBLIC API
  // =====================================

  return {

    // ==============================
    // INPUT
    // ==============================

    input,

    setInput,

    // ==============================
    // CONVERSATION
    // ==============================

    conversationState,

    // ==============================
    // ACTIONS
    // ==============================

    sendMessage,

    stopGeneration,

    handleKeyDown,

  };

}