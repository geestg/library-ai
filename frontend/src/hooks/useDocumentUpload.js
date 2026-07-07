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
  // HANDLE FILE UPLOAD
  // =====================================

  const handleFileUpload =
    useCallback(

      async (event) => {

        const files = Array.from(

          event.target.files || []

        );

        if (

          files.length === 0 ||

          !sessionId

        ) {

          event.target.value = "";

          return;

        }

        const requestGeneration =
          requestGenerationRef.current;

        for (const file of files) {

          const uploadId =
            `${Date.now()}-${file.name}`;

          // ===============================
          // SHOW UPLOADING STATE
          // ===============================

          setUploadingDocuments(

            previous => [

              ...previous,

              {

                id: uploadId,

                filename: file.name,

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

            if (

              requestGeneration !==
              requestGenerationRef.current

            ) {

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

            if (

              requestGeneration !==
              requestGenerationRef.current

            ) {

              continue;

            }

            console.error(

              "[DOCUMENT UPLOAD]",

              error

            );

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

            if (

              requestGeneration ===
              requestGenerationRef.current

            ) {

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

        }

        event.target.value = "";

      },

      [

        sessionId,

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