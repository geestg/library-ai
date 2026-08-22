import axios from "axios";
import { API_BASE_URL } from "./api";

const SESSION_API = `${API_BASE_URL}/session`;

// =====================================
// GET HISTORY LIST
// =====================================
export async function getSessionHistory() {
  try {
    const { data } = await axios.get(`${SESSION_API}/history`);
    return data;
  } catch (error) {
    console.error("[sessionApi] getSessionHistory Error:", error);
    return [];
  }
}

// =====================================
// CREATE
// =====================================
export async function createSession() {
  try {
    const { data } = await axios.post(`${SESSION_API}/create`);
    return data;
  } catch (error) {
    console.error("[sessionApi] createSession Error:", error);
    return null;
  }
}

// =====================================
// GET
// =====================================
export async function getSession(sessionId) {
  try {
    const { data } = await axios.get(`${SESSION_API}/${sessionId}`);
    return data;
  } catch (error) {
    console.error("[sessionApi] getSession Error:", error);
    return null;
  }
}

// =====================================
// DELETE
// =====================================
export async function deleteSession(sessionId) {
  try {
    const { data } = await axios.delete(`${SESSION_API}/${sessionId}`);
    return data;
  } catch (error) {
    console.error("[sessionApi] deleteSession Error:", error);
    return null;
  }
}