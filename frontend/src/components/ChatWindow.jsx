import { useState } from "react";
import api from "../services/api";

export default function ChatWindow() {

  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {

    if (!message) return;

    const userMessage = {
      role: "user",
      content: message
    };

    setMessages(prev => [...prev, userMessage]);

    const response = await api.post("/chat", {
      message
    });

    const aiMessage = {
      role: "assistant",
      content: response.data.response
    };

    setMessages(prev => [
      ...prev,
      aiMessage
    ]);

    setMessage("");
  };

  return (
    <div className="chat-window">

      <div className="messages">

        {messages.map((msg, index) => (

          <div
            key={index}
            className={`message ${msg.role}`}
          >
            {msg.content}
          </div>

        ))}

      </div>

      <div className="input-area">

        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Tanya apa saja..."
        />

        <button onClick={sendMessage}>
          Kirim
        </button>

      </div>

    </div>
  );
}