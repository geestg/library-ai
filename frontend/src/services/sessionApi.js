import axios from "axios";

import {
  API_BASE_URL,
} from "./api";

/* =====================================
   SESSION API
===================================== */

const SESSION_API_URL =
  API_BASE_URL;

/* =====================================
   CREATE SESSION
===================================== */

export async function createSession() {

  const {

    data,

  } = await axios.post(

    `${SESSION_API_URL}/session/create`

  );

  return data;

}

/* =====================================
   GET SESSION
===================================== */

export async function getSession({

  sessionId,

}) {

  const {

    data,

  } = await axios.get(

    (
      `${SESSION_API_URL}`
      + `/session/${sessionId}`
    )

  );

  return data;

}

/* =====================================
   DELETE SESSION
===================================== */

export async function deleteSession({

  sessionId,

}) {

  const {

    data,

  } = await axios.delete(

    (
      `${SESSION_API_URL}`
      + `/session/${sessionId}`
    )

  );

  return data;

}