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

  if (sessionId) {

    formData.append(
      "session_id",
      sessionId
    );

  }

  const {

    data

  } = await axios.post(

    `${DOCUMENT_API_URL}/upload-pdf`,

    formData,

    {

      headers: {

        "Content-Type":
          "multipart/form-data"

      }

    }

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