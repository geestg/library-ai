import {
  useState,
  useEffect,
  useRef,
  useCallback,
} from "react";

import {

  uploadDocument,

  listSessionDocuments,

  deleteSessionDocument,

  buildDocument,

  buildDocuments,

} from "../services/documentApi";

/* =====================================
   DOCUMENT UPLOAD HOOK
===================================== */

export default function useDocumentUpload({

  sessionId,

} = {}) {

  // =====================================
  // REQUEST GENERATION
  // =====================================

  const requestGenerationRef =
    useRef(0);

  // =====================================
  // DELETE LOCKS
  // =====================================

  const deletingDocumentIdsRef =
    useRef(
      new Set()
    );

  // =====================================
  // ACTIVE DOCUMENTS
  // =====================================

  const [

    activeDocuments,

    setActiveDocuments,

  ] = useState([]);

  // =====================================
  // UPLOADING DOCUMENTS
  // =====================================

  const [

    uploadingDocuments,

    setUploadingDocuments,

  ] = useState([]);

  // =====================================
  // DELETING DOCUMENTS
  // =====================================

  const [

    deletingDocumentIds,

    setDeletingDocumentIds,

  ] = useState(
    () => new Set()
  );

  // =====================================
  // DOCUMENT ERROR
  // =====================================

  const [

    documentError,

    setDocumentError,

  ] = useState(null);

  // =====================================
  // CLEAR DOCUMENT ERROR
  // =====================================

  const clearDocumentError =
    useCallback(() => {

      setDocumentError(null);

    }, []);

  // =====================================
  // CHECK DELETE STATE
  // =====================================

  const isDocumentDeleting =
    useCallback(

      (documentId) => {

        return deletingDocumentIds.has(
          documentId
        );

      },

      [

        deletingDocumentIds,

      ]

    );

  // =====================================
  // LOAD SESSION DOCUMENTS
  // =====================================

  const loadDocuments =
    useCallback(

      async () => {

        const requestGeneration =
          requestGenerationRef.current;

        if (!sessionId) {

          setActiveDocuments([]);

          return;

        }

        try {

          const response =
            await listSessionDocuments({

              sessionId,

            });

          if (

            requestGeneration !==
            requestGenerationRef.current

          ) {

            return;

          }

          setActiveDocuments(

            buildDocuments(

              response.documents || []

            )

          );

          setDocumentError(null);

        }

        catch (error) {

          if (

            requestGeneration !==
            requestGenerationRef.current

          ) {

            return;

          }

          console.error(

            "[DOCUMENT LIST]",

            error

          );

          setActiveDocuments([]);

          setDocumentError({

            type:
              "list",

            message:
              "Failed to load session documents.",

          });

        }

      },

      [

        sessionId,

      ]

    );

  // =====================================
  // SESSION DOCUMENT HYDRATION
  // =====================================

  useEffect(() => {

    requestGenerationRef.current += 1;

    deletingDocumentIdsRef.current =
      new Set();

    setActiveDocuments([]);

    setUploadingDocuments([]);

    setDeletingDocumentIds(
      new Set()
    );

    setDocumentError(null);

    loadDocuments();

    return () => {

      requestGenerationRef.current += 1;

      deletingDocumentIdsRef.current =
        new Set();

    };

  }, [

    loadDocuments,

  ]);

  // =====================================
  // REMOVE DOCUMENT
  // =====================================

  const removeDocument =
    useCallback(

      async (documentId) => {

        if (

          !sessionId ||

          !documentId

        ) {

          return;

        }

        // ===============================
        // DUPLICATE DELETE GUARD
        // ===============================

        if (

          deletingDocumentIdsRef.current.has(
            documentId
          )

        ) {

          return;

        }

        const requestGeneration =
          requestGenerationRef.current;

        const document =
          activeDocuments.find(

            item =>

              item.document_id ===
              documentId

          );

        // ===============================
        // LOCK DOCUMENT
        // ===============================

        deletingDocumentIdsRef.current.add(
          documentId
        );

        setDeletingDocumentIds(

          previous => {

            const next =
              new Set(previous);

            next.add(
              documentId
            );

            return next;

          }

        );

        try {

          await deleteSessionDocument({

            sessionId,

            documentId,

          });

          if (

            requestGeneration !==
            requestGenerationRef.current

          ) {

            return;

          }

          setActiveDocuments(

            previous =>

              previous.filter(

                item =>

                  item.document_id !==
                  documentId

              )

          );

          setDocumentError(null);

        }

        catch (error) {

          if (

            requestGeneration !==
            requestGenerationRef.current

          ) {

            return;

          }

          console.error(

            "[DOCUMENT DELETE]",

            error

          );

          setDocumentError({

            type:
              "delete",

            message:
              "Failed to delete document.",

            filename:
              document?.filename ??
              null,

            documentId,

          });

        }

        finally {

          if (

            requestGeneration ===
            requestGenerationRef.current

          ) {

            // ===============================
            // UNLOCK DOCUMENT
            // ===============================

            deletingDocumentIdsRef.current.delete(
              documentId
            );

            setDeletingDocumentIds(

              previous => {

                const next =
                  new Set(previous);

                next.delete(
                  documentId
                );

                return next;

              }

            );

          }

        }

      },

      [

        sessionId,

        activeDocuments,

      ]

    );

  // =====================================
  // CLEAR DOCUMENTS
  // =====================================

  const clearDocuments =
    useCallback(() => {

      requestGenerationRef.current += 1;

      deletingDocumentIdsRef.current =
        new Set();

      setActiveDocuments([]);

      setUploadingDocuments([]);

      setDeletingDocumentIds(
        new Set()
      );

      setDocumentError(null);

    }, []);

  // =====================================
  // CONSUME ACTIVE DOCUMENTS
  // =====================================

  const consumeActiveDocuments =
    useCallback(() => {

      // =================================
      // CLEAR COMPOSER ATTACHMENTS ONLY
      // =================================

      setActiveDocuments([]);

      setDocumentError(null);

    }, []);

  // =====================================
  // HANDLE FILE UPLOAD
  // =====================================

  const handleFileUpload =
    useCallback(

      async (event) => {

        // =================================
        // COPY FILES IMMEDIATELY
        // =================================

        const files = Array.from(
          event.target.files || []
        );

        // Reset input immediately.
        // Do not keep depending on the
        // synthetic event during async work.

        event.target.value = "";

        if (
          files.length === 0 ||
          !sessionId
        ) {

          return;

        }

        const requestGeneration =
          requestGenerationRef.current;

        console.log(
          "[DOCUMENT UPLOAD BATCH START]",
          {
            sessionId,

            totalFiles:
              files.length,

            files:
              files.map(
                file => file.name
              ),
          }
        );

        // =================================
        // UPLOAD FILES SEQUENTIALLY
        // =================================

        for (
          let index = 0;
          index < files.length;
          index += 1
        ) {

          const file =
            files[index];

          const uploadId =
            crypto.randomUUID();

          console.log(
            "[DOCUMENT UPLOAD START]",
            {
              index:
                index + 1,

              total:
                files.length,

              filename:
                file.name,

              uploadId,
            }
          );

          // ===============================
          // SHOW UPLOADING STATE
          // ===============================

          setUploadingDocuments(

            previous => [

              ...previous,

              {

                id:
                  uploadId,

                filename:
                  file.name,

              },

            ]

          );

          try {

            // ===============================
            // UPLOAD
            // ===============================

            const response =
              await uploadDocument({

                file,

                sessionId,

              });

            console.log(
              "[DOCUMENT UPLOAD SUCCESS]",
              {
                filename:
                  file.name,

                documentId:
                  response.document_id,

                sessionId:
                  response.session_id,
              }
            );

            // ===============================
            // STALE REQUEST GUARD
            // ===============================

            if (

              requestGeneration !==
              requestGenerationRef.current

            ) {

              console.warn(
                "[DOCUMENT UPLOAD STALE]",
                file.name
              );

              continue;

            }

            const document =
              buildDocument(
                response
              );

            // ===============================
            // STORE ACTIVE DOCUMENT
            // ===============================

            setActiveDocuments(

              previous => {

                const exists =
                  previous.some(

                    item =>

                      item.document_id ===
                      document.document_id

                  );

                if (exists) {

                  return previous;

                }

                return [

                  ...previous,

                  document,

                ];

              }

            );

            setDocumentError(null);

          }

          catch (error) {

            console.error(
              "[DOCUMENT UPLOAD FAILED]",
              {
                filename:
                  file.name,

                status:
                  error?.response?.status,

                data:
                  error?.response?.data,

                message:
                  error?.message,

                error,
              }
            );

            if (

              requestGeneration !==
              requestGenerationRef.current

            ) {

              continue;

            }

            setDocumentError({

              type:
                "upload",

              message:
                "Failed to upload document.",

              filename:
                file.name,

            });

          }

          finally {

            setUploadingDocuments(

              previous =>

                previous.filter(

                  item =>

                    item.id !==
                    uploadId

                )

            );

          }

        }

        // =================================
        // FINAL BACKEND SYNCHRONIZATION
        // =================================

        if (

          requestGeneration ===
          requestGenerationRef.current

        ) {

          console.log(
            "[DOCUMENT UPLOAD BATCH COMPLETE]",
            {
              sessionId,

              totalFiles:
                files.length,
            }
          );

          await loadDocuments();

        }

      },

      [

        sessionId,

        loadDocuments,

      ]

    );

  // =====================================
  // EXPORT
  // =====================================

  return {

    // ===============================
    // STATE
    // ===============================

    activeDocuments,

    uploadingDocuments,

    deletingDocumentIds,

    documentError,

    // ===============================
    // ACTIONS
    // ===============================

    handleFileUpload,

    removeDocument,

    clearDocuments,

    consumeActiveDocuments,

    loadDocuments,

    clearDocumentError,

    // ===============================
    // HELPERS
    // ===============================

    isDocumentDeleting,

    // ===============================
    // INTERNAL
    // ===============================

    setActiveDocuments,

  };

}