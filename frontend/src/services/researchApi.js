import axios from "axios";

import { API_BASE_URL }
from "./api";

const API_URL =
  `${API_BASE_URL}/api/research`;

export async function researchAnalysis(
  query,
  mode = "analysis"
) {
  const response =
    await axios.post(
      `${API_URL}/research-analysis`,
      {
        query,
        top_k: 5,
        mode
      }
    );

  return response.data;
}