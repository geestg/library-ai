import axios from "axios";

const API_URL =
  "http://localhost:8000/api/research";

export const researchAnalysis =
async (
    query,
    mode = "analysis"
) => {

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
};