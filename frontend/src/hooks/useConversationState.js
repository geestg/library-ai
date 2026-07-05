import { useCallback, useState } from "react";

// =====================================
// CONVERSATION STATES
// =====================================

export const ConversationState = Object.freeze({

  IDLE: "idle",

  THINKING: "thinking",

  STREAMING: "streaming",

  COMPLETED: "completed",

  CANCELLED: "cancelled",

  ERROR: "error",

});

// =====================================
// CONVERSATION STATE HOOK
// =====================================

export default function useConversationState() {

  const [

    conversationState,

    setConversationState,

  ] = useState(

    ConversationState.IDLE

  );

  // =====================================
  // TRANSITIONS
  // =====================================

  const setIdle = useCallback(() => {

    setConversationState(

      ConversationState.IDLE

    );

  }, []);

  const setThinking = useCallback(() => {

    setConversationState(

      ConversationState.THINKING

    );

  }, []);

  const setStreaming = useCallback(() => {

    setConversationState(

      ConversationState.STREAMING

    );

  }, []);

  const setCompleted = useCallback(() => {

    setConversationState(

      ConversationState.COMPLETED

    );

  }, []);

  const setCancelled = useCallback(() => {

    setConversationState(

      ConversationState.CANCELLED

    );

  }, []);

  const setError = useCallback(() => {

    setConversationState(

      ConversationState.ERROR

    );

  }, []);

  const reset = useCallback(() => {

    setConversationState(

      ConversationState.IDLE

    );

  }, []);

  // =====================================
  // FLAGS
  // =====================================

  const isIdle =
    conversationState ===
    ConversationState.IDLE;

  const isThinking =
    conversationState ===
    ConversationState.THINKING;

  const isStreaming =
    conversationState ===
    ConversationState.STREAMING;

  const isCompleted =
    conversationState ===
    ConversationState.COMPLETED;

  const isCancelled =
    conversationState ===
    ConversationState.CANCELLED;

  const isError =
    conversationState ===
    ConversationState.ERROR;

  // =====================================
  // PUBLIC API
  // =====================================

  return {

    conversationState,

    isIdle,

    isThinking,

    isStreaming,

    isCompleted,

    isCancelled,

    isError,

    setIdle,

    setThinking,

    setStreaming,

    setCompleted,

    setCancelled,

    setError,

    reset,

  };

}