import { useEffect, useState } from "react";

import useSession from "./useSession";

import {
  createEmptyResearchProfile,
} from "../services/researchApi";

const STORAGE_KEY = "delbot_workspace";

export default function useWorkspace() {

  // =====================================
  // SESSION
  // =====================================

  const {

    sessionId,

  } = useSession();

  // =====================================
  // CONVERSATION
  // =====================================

  const [

    messages,

    setMessages,

  ] = useState([]);

  // =====================================
  // SOURCES
  // =====================================

  const [

    sources,

    setSources,

  ] = useState([]);

  // =====================================
  // RESEARCH PROFILE
  // =====================================

  const [

    researchProfile,

    setResearchProfile,

  ] = useState(

    createEmptyResearchProfile()

  );

  // =====================================
  // LEGACY STATE
  // =====================================

  const [

    evidence,

    setEvidence,

  ] = useState({});

  const [

    evidenceMatrix,

    setEvidenceMatrix,

  ] = useState({});

  const [

    gapAnalysis,

    setGapAnalysis,

  ] = useState({});

  // =====================================
  // UI
  // =====================================

  const [

    activeCitation,

    setActiveCitation,

  ] = useState(null);

  const [

    selectedThesis,

    setSelectedThesis,

  ] = useState(null);

  // =====================================
  // RESTORE WORKSPACE
  // =====================================

  useEffect(() => {

    try {

      const raw = localStorage.getItem(
        STORAGE_KEY
      );

      if (!raw) {

        return;

      }

      const workspace = JSON.parse(
        raw
      );

      setMessages(

        workspace.messages ?? []

      );

      setSources(

        workspace.sources ?? []

      );

      setEvidence(

        workspace.evidence ?? {}

      );

      setEvidenceMatrix(

        workspace.evidenceMatrix ?? {}

      );

      setGapAnalysis(

        workspace.gapAnalysis ?? {}

      );

      setResearchProfile(

        workspace.researchProfile ??

        createEmptyResearchProfile()

      );

      console.info(
        "[Workspace] restored"
      );

    }

    catch (error) {

      console.error(

        "[Workspace Restore]",

        error

      );

      localStorage.removeItem(
        STORAGE_KEY
      );

    }

  }, []);

  // =====================================
  // PERSIST
  // =====================================

  useEffect(() => {

    localStorage.setItem(

      STORAGE_KEY,

      JSON.stringify({

        messages,

        sources,

        evidence,

        evidenceMatrix,

        gapAnalysis,

        researchProfile,

      })

    );

  }, [

    messages,

    sources,

    evidence,

    evidenceMatrix,

    gapAnalysis,

    researchProfile,

  ]);

  // =====================================
  // EXPORT
  // =====================================

  return {

    // ==============================
    // SESSION
    // ==============================

    sessionId,

    // ==============================
    // CONVERSATION
    // ==============================

    messages,

    setMessages,

    // ==============================
    // SOURCES
    // ==============================

    sources,

    setSources,

    // ==============================
    // RESEARCH PROFILE
    // ==============================

    researchProfile,

    setResearchProfile,

    // ==============================
    // LEGACY
    // ==============================

    evidence,

    setEvidence,

    evidenceMatrix,

    setEvidenceMatrix,

    gapAnalysis,

    setGapAnalysis,

    // ==============================
    // UI
    // ==============================

    activeCitation,

    setActiveCitation,

    selectedThesis,

    setSelectedThesis,

  };

}