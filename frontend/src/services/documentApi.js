import axios from "axios";

import {
  API_BASE_URL
} from "./api";

/* =====================================
   DOCUMENT API
===================================== */

const DOCUMENT_API_URL =
  API_BASE_URL;

/* =====================================
   UPLOAD DOCUMENT
===================================== */

export async function uploadDocument({

  file,

  sessionId,

}) {

  const formData =
    new FormData();

  formData.append(
    "file",
    file
  );

  formData.append(
    "session_id",
    sessionId
  );

  const uploadUrl =
    `${DOCUMENT_API_URL}/upload-pdf`;

  // =====================================
  // DEBUG
  // =====================================

  console.log(

    "[UPLOAD DEBUG]",

    {

      uploadUrl,

      apiBaseUrl:
        API_BASE_URL,

      documentApiUrl:
        DOCUMENT_API_URL,

      sessionId,

      filename:
        file?.name,

      fileSize:
        file?.size,

      fileType:
        file?.type,

      currentStoredSession:
        localStorage.getItem(
          "workspace_session_id"
        ),

    }

  );

  const {

    data

  } = await axios.post(

    uploadUrl,

    formData

  );

  return data;

}

/* =====================================
   UPLOAD MULTIPLE DOCUMENTS
===================================== */

export async function uploadDocuments({

  files = [],

  sessionId,

}) {

  const uploaded = [];

  for (const file of files) {

    const result =
      await uploadDocument({

        file,

        sessionId,

      });

    uploaded.push(
      result
    );

  }

  return uploaded;

}

/* =====================================
   LIST SESSION DOCUMENTS
===================================== */

export async function listSessionDocuments({

  sessionId,

}) {

  const listUrl =

    (
      `${DOCUMENT_API_URL}`
      + `/session/${sessionId}`
      + "/documents"
    );

  console.log(

    "[DOCUMENT LIST DEBUG]",

    {

      listUrl,

      sessionId,

      currentStoredSession:
        localStorage.getItem(
          "workspace_session_id"
        ),

    }

  );

  const {

    data

  } = await axios.get(

    listUrl

  );

  return data;

}

/* =====================================
   DELETE SESSION DOCUMENT
===================================== */

export async function deleteSessionDocument({

  sessionId,

  documentId,

}) {

  const {

    data

  } = await axios.delete(

    (
      `${DOCUMENT_API_URL}`
      + `/session/${sessionId}`
      + `/documents/${documentId}`
    )

  );

  return data;

}

/* =====================================
   FORMAT DOCUMENT
===================================== */

export function buildDocument(
  response
) {

  return {

    document_id:

      response.document_id,

    filename:

      response.filename,

    file_type:

      response.file_type ||

      "unknown",

    pages:

      response.pages ?? 0,

    chunks:

      response.chunks ?? 0,

    session_id:

      response.session_id ?? null,

    status:

      "ready",

  };

}

/* =====================================
   BUILD DOCUMENT LIST
===================================== */

export function buildDocuments(
  responses = []
) {

  return responses.map(

    buildDocument

  );

}