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

        if (

          abortControllerRef.current

        ) {

          console.info(

            "[STREAM LIFECYCLE] Aborting previous stream."

          );

          abortControllerRef.current.abort();

        }

        // ===============================
        // CREATE CONTROLLER
        // ===============================

        const controller =
          new AbortController();

        abortControllerRef.current =
          controller;

        streamingRef.current =
          true;

        console.info(

          "[STREAM LIFECYCLE] Stream started.",

          {

            sessionId,

            activeDocumentIds,

          }

        );

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

          console.info(

            "[STREAM LIFECYCLE] Stream completed normally."

          );

        }

        catch (error) {

          // ===============================
          // ABORT IS NOT AN APPLICATION ERROR
          // ===============================

          if (

            error?.name ===
            "AbortError"

          ) {

            console.info(

              "[STREAM LIFECYCLE] Abort received."

            );

            return;

          }

          console.error(

            "[STREAM LIFECYCLE] Stream failed.",

            error

          );

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

            console.info(

              "[STREAM LIFECYCLE] Stream cleaned up."

            );

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

      const controller =
        abortControllerRef.current;

      if (!controller) {

        console.info(

          "[STREAM LIFECYCLE] Stop ignored. No active stream."

        );

        return;

      }

      console.info(

        "[STREAM LIFECYCLE] Stop requested."

      );

      controller.abort();

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