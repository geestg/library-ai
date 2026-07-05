import { useCallback } from "react";

// =====================================
// WORKSPACE UPDATER
// =====================================

export default function useWorkspaceUpdater({

  setSources,

  setEvidence,

  setEvidenceMatrix,

  setGapAnalysis,

  setResearchProfile,

  setActiveCitation,

}) {

  // =====================================
  // CLEAR SELECTION
  // =====================================

  const clearSelection =
    useCallback(() => {

      setActiveCitation?.(null);

    }, [

      setActiveCitation,

    ]);

  // =====================================
  // UPDATE WORKSPACE
  // =====================================

  const updateWorkspace =
    useCallback(

      (context = {}) => {

        setResearchProfile?.(

          context.research_profile ?? {}

        );

        setSources?.(

          context.sources ?? []

        );

        setEvidence?.(

          context.evidence ?? {}

        );

        setEvidenceMatrix?.(

          context.evidence_matrix ?? {}

        );

        setGapAnalysis?.(

          context.research_profile?.gap ?? {}

        );

      },

      [

        setResearchProfile,

        setSources,

        setEvidence,

        setEvidenceMatrix,

        setGapAnalysis,

      ]

    );

  // =====================================
  // PUBLIC API
  // =====================================

  return {

    clearSelection,

    updateWorkspace,

  };

}