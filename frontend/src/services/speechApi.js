import { API_BASE_URL } from "./api";

export async function synthesizeSpeech(text, lang = "id") {
  try {
    const response = await fetch(`${API_BASE_URL}/speech/tts`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text, lang }),
    });

    if (!response.ok) {
      throw new Error(`TTS HTTP error! Status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("[speechApi] synthesizeSpeech Error:", error);
    return { status: "error", message: error.message };
  }
}

export async function transcribeSpeech(audioBase64) {
  try {
    const response = await fetch(`${API_BASE_URL}/speech/stt`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ audio_base64: audioBase64 }),
    });

    if (!response.ok) {
      throw new Error(`STT HTTP error! Status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("[speechApi] transcribeSpeech Error:", error);
    return { status: "error", message: error.message };
  }
}
