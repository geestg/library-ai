import {
  useState,
  useCallback,
} from "react";

import {

  uploadDocument,

  buildDocument,

} from "../services/documentApi";

/* =====================================
   DOCUMENT UPLOAD HOOK
===================================== */

export default function useDocumentUpload({

  sessionId,

} = {}) {

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
  // REMOVE DOCUMENT
  // =====================================

  const removeDocument =
    useCallback(

      (documentId) => {

        setActiveDocuments(

          previous =>

            previous.filter(

              document =>

                document.document_id !==
                documentId

            )

        );

      },

      []

    );

  // =====================================
  // CLEAR DOCUMENTS
  // =====================================

  const clearDocuments =
    useCallback(() => {

      setActiveDocuments([]);

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

        if (files.length === 0) {

          return;

        }

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

            // ===============================
            // REMOVE LOADING
            // ===============================

            setUploadingDocuments(

              previous =>

                previous.filter(

                  item =>

                    item.id !==
                    uploadId

                )

            );

            // ===============================
            // STORE ACTIVE DOCUMENT
            // ===============================

            setActiveDocuments(

              previous => [

                ...previous,

                buildDocument(
                  response
                ),

              ]

            );

          }

          catch (error) {

            console.error(

              "[DOCUMENT]",

              error

            );

            // ===============================
            // REMOVE FAILED UPLOAD
            // ===============================

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
        // RESET INPUT
        // =================================

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

    // ===============================
    // ACTIONS
    // ===============================

    handleFileUpload,

    removeDocument,

    clearDocuments,

    // ===============================
    // INTERNAL
    // ===============================

    setActiveDocuments,

  };

}