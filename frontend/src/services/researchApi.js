import axios from "axios";

import {
  API_BASE_URL,
} from "./api";

const API_URL =
  `${API_BASE_URL}/api/research`;

/* =====================================
   RESEARCH ANALYSIS (LEGACY)
===================================== */

export async function researchAnalysis({

  query,

  mode = "analysis",

  topK = 10,

  activeDocumentIds = [],

}) {

  const payload = {

    query,

    mode,

    top_k:
      topK,

    active_document_ids:
      activeDocumentIds,

  };

  const {

    data,

  } = await axios.post(

    (
      `${API_URL}`
      + "/research-analysis"
    ),

    payload

  );

  return data;

}

/* =====================================
   STREAM RESEARCH ANALYSIS
===================================== */

export async function streamResearchAnalysis({

  sessionId,

  query,

  activeDocumentIds = [],

  signal,

  onStart,

  onMetadata,

  onProgress,

  onToken,

  onContext,

  onCitations,

  onSources,

  onResearchProfile,

  onEnd,

  onError,

}) {

  const response = await fetch(

    (
      `${API_BASE_URL}`
      + "/chat-stream"
    ),

    {

      method:
        "POST",

      headers: {

        "Content-Type":
          "application/json",

      },

      signal,

      body:
        JSON.stringify({

          session_id:
            sessionId,

          message:
            query,

          active_document_ids:
            activeDocumentIds,

        }),

    }

  );

  // =====================================
  // HTTP ERROR
  // =====================================

  if (!response.ok) {

    throw new Error(

      (
        "Streaming request failed "
        + `(${response.status})`
      )

    );

  }

  // =====================================
  // EMPTY STREAM
  // =====================================

  if (!response.body) {

    throw new Error(

      "Streaming response body is empty."

    );

  }

  // =====================================
  // STREAM READER
  // =====================================

  const reader =
    response.body.getReader();

  const decoder =
    new TextDecoder();

  let buffer = "";

  // =====================================
  // EVENT HANDLERS
  // =====================================

  const handlers = {

    onStart,

    onMetadata,

    onProgress,

    onToken,

    onContext,

    onResearchProfile,

    onSources,

    onCitations,

    onEnd,

    onError,

  };

  try {

    while (true) {

      const {

        value,

        done,

      } = await reader.read();

      if (done) {

        break;

      }

      // =================================
      // DECODE STREAM CHUNK
      // =================================

      buffer += decoder.decode(

        value,

        {

          stream:
            true,

        }

      );

      // =================================
      // SPLIT NDJSON LINES
      // =================================

      const lines =
        buffer.split("\n");

      buffer =
        lines.pop() ?? "";

      // =================================
      // PROCESS COMPLETE EVENTS
      // =================================

      for (const line of lines) {

        if (!line.trim()) {

          continue;

        }

        let event;

        try {

          event =
            JSON.parse(line);

        }

        catch (error) {

          console.error(

            "[STREAM] Invalid JSON",

            error,

            line

          );

          continue;

        }

        // ===============================
        // DISPATCH EVENT
        // ===============================

        dispatchStreamEvent(

          event,

          handlers

        );

      }

    }

    // ===================================
    // FLUSH DECODER
    // ===================================

    buffer += decoder.decode();

    // ===================================
    // PROCESS TRAILING EVENT
    // ===================================

    if (buffer.trim()) {

      try {

        dispatchStreamEvent(

          JSON.parse(buffer),

          handlers

        );

      }

      catch (error) {

        console.error(

          "[STREAM] Invalid trailing JSON",

          error,

          buffer

        );

      }

    }

  }

  finally {

    reader.releaseLock();

  }

}

/* =====================================
   STREAM DISPATCHER
===================================== */

function dispatchStreamEvent(

  event,

  handlers

) {

  // =====================================
  // INVALID EVENT GUARD
  // =====================================

  if (

    !event ||

    typeof event !== "object"

  ) {

    console.warn(

      "[STREAM] Invalid event:",

      event

    );

    return;

  }

  // =====================================
  // EVENT ROUTING
  // =====================================

  switch (event.type) {

    // ===================================
    // START
    // ===================================

    case "start":

      handlers.onStart?.(

        event.data

      );

      break;

    // ===================================
    // METADATA
    // ===================================

    case "metadata":

      handlers.onMetadata?.(

        event.data

      );

      break;

    // ===================================
    // PROGRESS
    // ===================================

    case "progress":

      handlers.onProgress?.(

        event.data

      );

      break;

    // ===================================
    // TOKEN
    // ===================================

    case "token":

      handlers.onToken?.(

        event.data

      );

      break;

    // ===================================
    // CONTEXT
    // ===================================

    case "context":

    case "context_final":

      handlers.onContext?.(

        event.data

      );

      break;

    // ===================================
    // RESEARCH PROFILE
    // ===================================

    case "research_profile":

      handlers.onResearchProfile?.(

        event.data

      );

      break;

    // ===================================
    // CITATIONS
    // ===================================

    case "citations":

      handlers.onCitations?.(

        event.data

      );

      break;

    // ===================================
    // SOURCES
    // ===================================

    case "sources":

      handlers.onSources?.(

        event.data

      );

      break;

    // ===================================
    // END
    // ===================================

    case "end":

      handlers.onEnd?.(

        event.data

      );

      break;

    // ===================================
    // ERROR
    // ===================================

    case "error":

      handlers.onError?.(

        event.data

      );

      break;

    // ===================================
    // UNKNOWN
    // ===================================

    default:

      console.warn(

        "[STREAM] Unknown event:",

        event.type,

        event

      );

  }

}

/* =====================================
   BUILD WORKSPACE CONTEXT
===================================== */

export function buildWorkspaceContext(

  context

) {

  return {

    researchProfile:

      context.research_profile ??

      createEmptyResearchProfile(),

    sources:

      context.sources ??

      context.related_theses ??

      [],

    citations:

      context.citations ??

      [],

    evidence:

      context.evidence ??

      {},

    evidenceMatrix:

      context.evidence_matrix ??

      {},

    gapAnalysis:

      context.research_profile?.gap ??

      {},

  };

}

/* =====================================
   PARSE RESEARCH PROFILE
===================================== */

export function buildResearchProfile(

  response

) {

  if (

    response.research_profile

  ) {

    return response.research_profile;

  }

  return {

    trend:

      response.trend_analysis ??

      {},

    gap:

      response.gap_analysis ??

      {},

    novelty:

      response.novelty_analysis ??

      {},

    competency:

      response.competency_analysis ??

      {},

    prodi:

      response.prodi_analysis ??

      {},

  };

}

/* =====================================
   PARSE ASSISTANT MESSAGE
===================================== */

export function buildAssistantMessage(

  response

) {

  const profile =
    buildResearchProfile(

      response

    );

  return {

    role:
      "assistant",

    content:

      response.analysis ||

      response.answer ||

      response.comparison ||

      "No response returned.",

    citations:

      response.citations ||

      [],

    evidence:

      response.evidence ||

      {},

    noveltyAnalysis:

      profile.novelty ||

      null,

  };

}

/* =====================================
   BUILD WORKSPACE STATE
===================================== */

export function buildWorkspaceState(

  response

) {

  const profile =
    buildResearchProfile(

      response

    );

  return {

    researchProfile:

      profile,

    sources:

      response.sources ??

      response.related_theses ??

      response.citations ??

      [],

    evidence:

      response.evidence ??

      {},

    evidenceMatrix:

      response.evidence_matrix ??

      {},

    gapAnalysis:

      profile.gap ??

      {},

  };

}

/* =====================================
   EMPTY RESEARCH PROFILE
===================================== */

export function createEmptyResearchProfile() {

  return {

    trend:
      {},

    gap:
      {},

    novelty:
      {},

    competency:
      {},

    prodi:
      {},

  };

}