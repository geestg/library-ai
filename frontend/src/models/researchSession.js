// =====================================
// RESEARCH SESSION MODEL
// =====================================

export function createResearchSession() {

  return {

    id:

      crypto.randomUUID(),

    title:

      "New Research Session",

    createdAt:

      new Date().toISOString(),

    updatedAt:

      new Date().toISOString(),

    // ===============================
    // CONVERSATION
    // ===============================

    conversation: [],

    // ===============================
    // RESEARCH PROFILE
    // ===============================

    researchProfile: {

      trend: {},

      gap: {},

      novelty: {},

      competency: {},

      prodi: {}

    },

    // ===============================
    // EVIDENCE
    // ===============================

    evidence: {

      sources: [],

      matrix: {},

      citations: []

    },

    // ===============================
    // ARTIFACTS
    // ===============================

    artifacts: [],

    // ===============================
    // DOCUMENTS
    // ===============================

    documents: [],

    // ===============================
    // TIMELINE
    // ===============================

    timeline: []

  };

}