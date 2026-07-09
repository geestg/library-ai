import {
  useEffect,
  useRef,
  useState,
} from "react";

import useSession from "./useSession";

import {
  createEmptyResearchProfile,
} from "../services/researchApi";

// =====================================
// STORAGE
// =====================================

const STORAGE_KEY_PREFIX =
  "delbot_workspace";

// =====================================
// EMPTY WORKSPACE FACTORY
// =====================================

function createEmptyWorkspace() {

  return {

    messages:
      [],

    sources:
      [],

    evidence:
      {},

    evidenceMatrix:
      {},

    gapAnalysis:
      {},

    researchProfile:
      createEmptyResearchProfile(),

  };

}

// =====================================
// SESSION STORAGE KEY
// =====================================

function getWorkspaceStorageKey(

  sessionId

) {

  return (

    `${STORAGE_KEY_PREFIX}:${sessionId}`

  );

}

// =====================================
// WORKSPACE HOOK
// =====================================

export default function useWorkspace() {

  // =====================================
  // SESSION
  // =====================================

  const {

    sessionId,

  } = useSession();

  // =====================================
  // HYDRATION
  // =====================================

  const [

    isWorkspaceHydrated,

    setIsWorkspaceHydrated,

  ] = useState(false);

  const hydratedSessionRef =
    useRef(null);

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
  // RESTORE SESSION WORKSPACE
  // =====================================

  useEffect(() => {

    // =================================
    // WAIT FOR SESSION
    // =================================

    if (!sessionId) {

      return;

    }

    // =================================
    // PREVENT DUPLICATE HYDRATION
    // =================================

    if (

      hydratedSessionRef.current ===
      sessionId

    ) {

      return;

    }

    // =================================
    // BEGIN HYDRATION
    // =================================

    setIsWorkspaceHydrated(
      false
    );

    const storageKey =

      getWorkspaceStorageKey(

        sessionId

      );

    try {

      // =================================
      // RESET SESSION-BOUND STATE
      // =================================

      const emptyWorkspace =
        createEmptyWorkspace();

      setMessages(

        emptyWorkspace.messages

      );

      setSources(

        emptyWorkspace.sources

      );

      setEvidence(

        emptyWorkspace.evidence

      );

      setEvidenceMatrix(

        emptyWorkspace.evidenceMatrix

      );

      setGapAnalysis(

        emptyWorkspace.gapAnalysis

      );

      setResearchProfile(

        emptyWorkspace.researchProfile

      );

      // =================================
      // RESET TRANSIENT UI STATE
      // =================================

      setActiveCitation(
        null
      );

      setSelectedThesis(
        null
      );

      // =================================
      // READ SESSION WORKSPACE
      // =================================

      const raw =

        localStorage.getItem(

          storageKey

        );

      if (raw) {

        const workspace =

          JSON.parse(

            raw

          );

        setMessages(

          workspace.messages ??
          []

        );

        setSources(

          workspace.sources ??
          []

        );

        setEvidence(

          workspace.evidence ??
          {}

        );

        setEvidenceMatrix(

          workspace.evidenceMatrix ??
          {}

        );

        setGapAnalysis(

          workspace.gapAnalysis ??
          {}

        );

        setResearchProfile(

          workspace.researchProfile ??

          createEmptyResearchProfile()

        );

        console.info(

          "[Workspace] restored",

          {

            sessionId,

            storageKey,

          }

        );

      }

      else {

        console.info(

          "[Workspace] initialized",

          {

            sessionId,

            storageKey,

          }

        );

      }

    }

    catch (error) {

      console.error(

        "[Workspace Restore]",

        {

          sessionId,

          storageKey,

          error,

        }

      );

      // =================================
      // REMOVE ONLY CORRUPTED SESSION
      // =================================

      localStorage.removeItem(

        storageKey

      );

      // =================================
      // FALL BACK TO EMPTY WORKSPACE
      // =================================

      const emptyWorkspace =
        createEmptyWorkspace();

      setMessages(

        emptyWorkspace.messages

      );

      setSources(

        emptyWorkspace.sources

      );

      setEvidence(

        emptyWorkspace.evidence

      );

      setEvidenceMatrix(

        emptyWorkspace.evidenceMatrix

      );

      setGapAnalysis(

        emptyWorkspace.gapAnalysis

      );

      setResearchProfile(

        emptyWorkspace.researchProfile

      );

      setActiveCitation(
        null
      );

      setSelectedThesis(
        null
      );

    }

    finally {

      // =================================
      // MARK SESSION AS HYDRATED
      // =================================

      hydratedSessionRef.current =
        sessionId;

      setIsWorkspaceHydrated(
        true
      );

    }

  }, [

    sessionId,

  ]);

  // =====================================
  // PERSIST SESSION WORKSPACE
  // =====================================

  useEffect(() => {

    // =================================
    // REQUIRE SESSION
    // =================================

    if (!sessionId) {

      return;

    }

    // =================================
    // REQUIRE COMPLETED HYDRATION
    // =================================

    if (!isWorkspaceHydrated) {

      return;

    }

    // =================================
    // REQUIRE MATCHING SESSION
    // =================================

    if (

      hydratedSessionRef.current !==
      sessionId

    ) {

      return;

    }

    const storageKey =

      getWorkspaceStorageKey(

        sessionId

      );

    try {

      localStorage.setItem(

        storageKey,

        JSON.stringify({

          messages,

          sources,

          evidence,

          evidenceMatrix,

          gapAnalysis,

          researchProfile,

        })

      );

    }

    catch (error) {

      console.error(

        "[Workspace Persist]",

        {

          sessionId,

          storageKey,

          error,

        }

      );

    }

  }, [

    sessionId,

    isWorkspaceHydrated,

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
    // HYDRATION
    // ==============================

    isWorkspaceHydrated,

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