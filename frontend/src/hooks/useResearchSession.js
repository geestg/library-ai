import {
  useState,
  useCallback,
  useRef,
} from "react";

import useConversationState from "./useConversationState";

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
  // STREAM PROGRESS
  // =====================================

  const [

    streamProgress,

    setStreamProgress,

  ] = useState(null);

  // =====================================
  // INTERNAL SEND LOCK
  // =====================================

  const sendingRef =
    useRef(false);

  // =====================================
  // CONVERSATION STATE
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
  // ASSISTANT MESSAGE
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
      // REQUIRE SESSION
      // =================================

      if (!sessionId) {

        console.warn(

          "[ResearchSession] Session is not ready."

        );

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

      // =================================
      // RESET STREAM PROGRESS
      // =================================

      setStreamProgress(null);

      // =================================
      // CLEAR UI SELECTION
      // =================================

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

          onStart(data) {

            setThinking();

            setStreamProgress(

              data ?? null

            );

          },

          // =============================
          // METADATA
          // =============================

          onMetadata(metadata) {

            console.info(

              "[STREAM METADATA]",

              metadata

            );

          },

          // =============================
          // PROGRESS
          // =============================

          onProgress(progress) {

            console.info(

              "[STREAM PROGRESS]",

              progress

            );

            setStreamProgress(

              progress ?? null

            );

          },

          // =============================
          // TOKEN
          // =============================

          onToken(token) {

            // First token means the
            // assistant is now streaming.

            setStreaming();

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

          onEnd(data) {

            // ===========================
            // UNLOCK SEND
            // ===========================

            sendingRef.current =
              false;

            // ===========================
            // FINAL PROGRESS
            // ===========================

            setStreamProgress(

              data ?? null

            );

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

              "[STREAM ERROR]",

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

            setStreamProgress(null);

            setError();

          },

        });

      }

      catch (error) {

        // =================================
        // ABORT
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

          setStreamProgress(null);

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

            (
              "Terjadi error saat "
              + "memproses request.\n\n"
              + (
                error?.message ??
                "Unknown error"
              )
            ),

        });

        // =================================
        // KEEP DOCUMENTS FOR RETRY
        // =================================

        sendingRef.current =
          false;

        setStreamProgress(null);

        setError();

      }

    }, [

      sessionId,

      input,

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

      // =================================
      // ABORT ACTIVE REQUEST
      // =================================

      stopStream();

      // =================================
      // UNLOCK SEND
      // =================================

      sendingRef.current =
        false;

      // =================================
      // CLEAR PROGRESS
      // =================================

      setStreamProgress(null);

      // =================================
      // CANCEL CONVERSATION
      // =================================

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

      event => {

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
    // STREAM PROGRESS
    // ==============================

    streamProgress,

    // ==============================
    // ACTIONS
    // ==============================

    sendMessage,

    stopGeneration,

    handleKeyDown,

  };

}