import { useCallback } from "react";

// =====================================
// ASSISTANT MESSAGE HOOK
// =====================================

export default function useAssistantMessage({

  setMessages,

}) {

  // =====================================
  // APPEND USER + EMPTY ASSISTANT
  // =====================================

  const appendConversation =
    useCallback(

      (

        userMessage,

        attachedDocuments = []

      ) => {

        setMessages(

          (previous) => [

            ...previous,

            {

              role: "user",

              content:
                userMessage,

              attachedDocuments,

            },

            {

              role: "assistant",

              content: "",

              citations: [],

              evidence: {},

              noveltyAnalysis:
                null,

            },

          ]

        );

      },

      [

        setMessages,

      ]

    );

  // =====================================
  // APPEND STREAM TOKEN
  // =====================================

  const appendToken =
    useCallback(

      (token) => {

        setMessages(

          (previous) => {

            if (
              previous.length === 0
            ) {

              return previous;

            }

            const updated = [
              ...previous
            ];

            const index =
              updated.length - 1;

            updated[index] = {

              ...updated[index],

              content:

                (
                  updated[index]
                    .content ??
                  ""
                ) + token,

            };

            return updated;

          }

        );

      },

      [

        setMessages,

      ]

    );

  // =====================================
  // PATCH LAST ASSISTANT MESSAGE
  // =====================================

  const patchAssistant =
    useCallback(

      (patch) => {

        setMessages(

          (previous) => {

            if (
              previous.length === 0
            ) {

              return previous;

            }

            const updated = [
              ...previous
            ];

            const index =
              updated.length - 1;

            updated[index] = {

              ...updated[index],

              ...patch,

            };

            return updated;

          }

        );

      },

      [

        setMessages,

      ]

    );

  // =====================================
  // REPLACE LAST ASSISTANT
  // =====================================

  const replaceAssistant =
    useCallback(

      (assistant) => {

        setMessages(

          (previous) => {

            if (
              previous.length === 0
            ) {

              return previous;

            }

            const updated = [
              ...previous
            ];

            updated[
              updated.length - 1
            ] = assistant;

            return updated;

          }

        );

      },

      [

        setMessages,

      ]

    );

  // =====================================
  // CLEAR ASSISTANT CONTENT
  // =====================================

  const clearAssistant =
    useCallback(

      () => {

        patchAssistant({

          content: "",

          citations: [],

          evidence: {},

          noveltyAnalysis:
            null,

        });

      },

      [

        patchAssistant,

      ]

    );

  // =====================================
  // APPEND CITATIONS
  // =====================================

  const updateCitations =
    useCallback(

      (citations) => {

        patchAssistant({

          citations,

        });

      },

      [

        patchAssistant,

      ]

    );

  // =====================================
  // APPEND EVIDENCE
  // =====================================

  const updateEvidence =
    useCallback(

      (evidence) => {

        patchAssistant({

          evidence,

        });

      },

      [

        patchAssistant,

      ]

    );

  // =====================================
  // APPEND NOVELTY
  // =====================================

  const updateNovelty =
    useCallback(

      (noveltyAnalysis) => {

        patchAssistant({

          noveltyAnalysis,

        });

      },

      [

        patchAssistant,

      ]

    );

  // =====================================
  // PUBLIC API
  // =====================================

  return {

    appendConversation,

    appendToken,

    patchAssistant,

    replaceAssistant,

    clearAssistant,

    updateCitations,

    updateEvidence,

    updateNovelty,

  };

}