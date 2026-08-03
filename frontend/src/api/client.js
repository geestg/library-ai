import axios from "axios";
import { APP_CONFIG } from "../config/app";
export const api = axios.create({
    baseURL: APP_CONFIG.API_BASE_URL,
    timeout: 60000,
    headers: {
        "Content-Type": "application/json",
    },
});
