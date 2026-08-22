import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE_URL
});

api.interceptors.request.use((config) => {
  const role = localStorage.getItem("userRole") || "student";
  config.headers["X-User-Role"] = role;
  return config;
}, (error) => {
  return Promise.reject(error);
});

export default api;

export { API_BASE_URL };