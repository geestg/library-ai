import {
  useCallback,
  useRef,
} from "react";

import {
  streamResearchAnalysis,
} from "../services/researchApi";

// =====================================
// STREAMING CHAT
// =====================================

export default function useStreamingChat() {

  // =====================================
  // ABORT CONTROLLER
  // =====================================

  const abortControllerRef =
    useRef(null);

  // =====================================
  // STREAM STATUS
  // =====================================

  const streamingRef =
    useRef(false);

  // =====================================
  // START STREAM
  // =====================================

  const startStream =
    useCallback(

      async ({

        // ===============================
        // REQUEST
        // ===============================

        sessionId,

        query,

        activeDocumentIds = [],

        // ===============================
        // CORE STREAM EVENTS
        // ===============================

        onStart,

        onMetadata,

        onProgress,

        onToken,

        // ===============================
        // CONTEXT
        // ===============================

        onContext,

        // ===============================
        // LEGACY / COMPATIBILITY
        // ===============================

        onResearchProfile,

        onSources,

        onCitations,

        // ===============================
        // LIFECYCLE
        // ===============================

        onEnd,

        onError,

      }) => {

        // ===============================
        // CANCEL PREVIOUS STREAM
        // ===============================

        abortControllerRef.current?.abort();

        // ===============================
        // CREATE CONTROLLER
        // ===============================

        const controller =
          new AbortController();

        abortControllerRef.current =
          controller;

        streamingRef.current =
          true;

        try {

          await streamResearchAnalysis({

            // ===========================
            // REQUEST
            // ===========================

            sessionId,

            query,

            activeDocumentIds,

            signal:
              controller.signal,

            // ===========================
            // CORE STREAM EVENTS
            // ===========================

            onStart,

            onMetadata,

            onProgress,

            onToken,

            // ===========================
            // CONTEXT
            // ===========================

            onContext,

            // ===========================
            // LEGACY / COMPATIBILITY
            // ===========================

            onResearchProfile,

            onSources,

            onCitations,

            // ===========================
            // LIFECYCLE
            // ===========================

            onEnd,

            onError,

          });

        }

        catch (error) {

          // ===============================
          // ABORT IS NOT AN APPLICATION ERROR
          // ===============================

          if (
            error?.name ===
            "AbortError"
          ) {

            return;

          }

          throw error;

        }

        finally {

          // ===============================
          // ONLY CLEAR CURRENT CONTROLLER
          // ===============================

          if (

            abortControllerRef.current ===
            controller

          ) {

            streamingRef.current =
              false;

            abortControllerRef.current =
              null;

          }

        }

      },

      []

    );

  // =====================================
  // STOP STREAM
  // =====================================

  const stopStream =
    useCallback(() => {

      abortControllerRef.current?.abort();

    }, []);

  // =====================================
  // CHECK STREAM STATUS
  // =====================================

  const isStreaming =
    useCallback(() => {

      return streamingRef.current;

    }, []);

  // =====================================
  // PUBLIC API
  // =====================================

  return {

    startStream,

    stopStream,

    isStreaming,

  };

}