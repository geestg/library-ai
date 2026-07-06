import axios from "axios";

import {
  API_BASE_URL
} from "./api";

const SESSION_API =
  `${API_BASE_URL}/session`;

// =====================================
// CREATE
// =====================================

export async function createSession() {

  const {

    data

  } = await axios.post(

    `${SESSION_API}/create`

  );

  return data;

}

// =====================================
// GET
// =====================================

export async function getSession(

  sessionId

) {

  const {

    data

  } = await axios.get(

    `${SESSION_API}/${sessionId}`

  );

  return data;

}

// =====================================
// DELETE
// =====================================

export async function deleteSession(

  sessionId

) {

  const {

    data

  } = await axios.delete(

    `${SESSION_API}/${sessionId}`

  );

  return data;

}