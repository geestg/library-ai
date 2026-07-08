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

  sessionId,

  activeDocuments = [],

  setMessages,

  setSources,

  setEvidence,

  setEvidenceMatrix,

  setGapAnalysis,

  setResearchProfile,

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

      const finalInput =
        input.trim();

      if (!finalInput) {

        return;

      }

      if (sendingRef.current) {

        return;

      }

      sendingRef.current = true;

      reset();

      setThinking();

      clearSelection();

      appendConversation(

        finalInput,

        activeDocuments

      );

      setInput("");

      // =================================
      // BUILD ACTIVE DOCUMENT IDS
      // =================================

      const activeDocumentIds =

        activeDocuments.map(

          (document) =>

            document.document_id

        );

      // =================================
      // SEND MESSAGE DEBUG
      // =================================

      console.log(

        "[SEND MESSAGE DEBUG]",

        {

          sessionId,

          finalInput,

          totalActiveDocuments:
            activeDocuments.length,

          activeDocuments,

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

            sendingRef.current = false;

            setCompleted();

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

            sendingRef.current = false;

            setError();

          },

        });

      }

      catch (error) {

        // =============================
        // STOP GENERATION
        // =============================

        if (

          error?.name ===

          "AbortError"

        ) {

          sendingRef.current = false;

          setCancelled();

          return;

        }

        console.error(

          "[ResearchSession]",

          error

        );

        patchAssistant({

          content:

            `Terjadi error saat memproses request.\n\n${error.message}`,

        });

        sendingRef.current = false;

        setError();

      }

    }, [

      sessionId,

      input,

      conversationState,

      activeDocuments,

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

      sendingRef.current = false;

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