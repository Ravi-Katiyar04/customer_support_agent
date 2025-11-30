import React, { useState, useRef, useEffect } from "react";
import "./chat.css"; // <-- import the CSS file

export default function Chat() {
  const [sessionId] = useState(() => {
    const existing = localStorage.getItem("esa_session_id");
    if (existing) return existing;
    const id = `sess_${Date.now().toString(36)}`;
    localStorage.setItem("esa_session_id", id);
    return id;
  });

  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");
  const [typing, setTyping] = useState(false);

  const chatRef = useRef(null);

  // Auto-scroll
  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages, typing]);

  function timestamp() {
    return new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  }

  // Send message
  async function send() {
    if (!text.trim()) return;

    setMessages((m) => [...m, { from: "You", text, time: timestamp() }]);
    setText("");
    setTyping(true);

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/message`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, text }),
      });


      const data = await res.json();
      setTyping(false);

      if (data.responses) {
        data.responses.forEach((r) =>
          setMessages((m) => [
            ...m,
            { from: "Agent", text: r, time: timestamp() },
          ])
        );
      }

      if (data.approvals) {
        data.approvals.forEach(() =>
          setMessages((m) => [
            ...m,
            { from: "SYSTEM", text: "Pending approval required", time: timestamp() },
          ])
        );
      }
    } catch (e) {
      setTyping(false);
      setMessages((m) => [
        ...m,
        { from: "System", text: "Error contacting backend", time: timestamp() },
      ]);
    }
  }

  return (
    <div className="chat-container">
      <div className="chat-header">ESA — Customer Support</div>

      <div className="chat-box" ref={chatRef}>
        {messages.map((m, i) => (
          <div
            key={i}
            className={`msg-row ${m.from === "You" ? "right" : "left"}`}
          >
            <div className={`msg-bubble ${m.from}`}>
              <div className="msg-meta">
                {m.from} • {m.time}
              </div>
              {m.text}
            </div>
          </div>
        ))}

        {typing && (
          <div className="typing">
            <div className="typing-bubble">
              <span className="dot"></span>
              <span className="dot"></span>
              <span className="dot"></span>
            </div>
          </div>
        )}
      </div>

      {/* Input Section */}
      <div className="input-area">
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Type your message..."
          className="chat-input"
        />

        <button onClick={send} className="send-btn">
          Send
        </button>
      </div>
    </div>
  );
}

