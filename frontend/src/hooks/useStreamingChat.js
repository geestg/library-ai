import { useCallback, useRef } from "react";

import {
  streamResearchAnalysis,
} from "../services/researchApi";

// =====================================
// STREAMING CHAT
// =====================================

export default function useStreamingChat() {

  const abortControllerRef =
    useRef(null);

  const streamingRef =
    useRef(false);

  // =====================================
  // START STREAM
  // =====================================

  const startStream =
    useCallback(

      async ({

        sessionId,

        query,

        activeDocumentIds = [],

        onStart,

        onMetadata,

        onToken,

        // =============================
        // NEW
        // =============================

        onContext,

        // =============================
        // LEGACY
        // =============================

        onResearchProfile,

        onSources,

        onCitations,

        onEnd,

        onError,

      }) => {

        abortControllerRef.current =
          new AbortController();

        streamingRef.current =
          true;

        try {

          await streamResearchAnalysis({

            sessionId,

            query,

            activeDocumentIds,

            signal:
              abortControllerRef.current.signal,

            onStart,

            onMetadata,

            onToken,

            // =========================
            // NEW
            // =========================

            onContext,

            // =========================
            // LEGACY
            // =========================

            onResearchProfile,

            onSources,

            onCitations,

            onEnd,

            onError,

          });

        }

        catch (error) {

          if (
            error.name ===
            "AbortError"
          ) {

            return;

          }

          throw error;

        }

        finally {

          streamingRef.current =
            false;

          abortControllerRef.current =
            null;

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
  // STREAM STATUS
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