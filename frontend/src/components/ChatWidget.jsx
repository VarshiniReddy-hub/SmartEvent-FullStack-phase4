import { useState } from "react";
import axios from "axios";

const API = "http://127.0.0.1:8000/api/v1";

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([{ from: "bot", text: "Hi! I can help you discover events or check your bookings." }]);
  const [busy, setBusy] = useState(false);

  async function send(text = message) {
    const clean = text.trim();
    if (!clean || busy) return;
    const token = localStorage.getItem("access_token");
    setMessages(old => [...old, { from: "user", text: clean }]);
    setMessage("");
    if (!token) {
      setMessages(old => [...old, { from: "bot", text: "Please log in first to use the assistant." }]);
      return;
    }
    setBusy(true);
    try {
      const response = await axios.post(`${API}/chat`, { message: clean }, { headers: { Authorization: `Bearer ${token}` } });
      const data = response.data;
      const eventText = (data.events || []).map(e => `${e.title} — ${e.location}, ₹${e.ticket_price}`).join("\n");
      const bookingText = (data.bookings || []).map(b => `Booking #${b.booking_id}: ${b.event} (${b.status})`).join("\n");
      setMessages(old => [...old, { from: "bot", text: [data.reply, eventText, bookingText].filter(Boolean).join("\n") }]);
    } catch (error) {
      setMessages(old => [...old, { from: "bot", text: error.response?.data?.detail || "I couldn't process that. Please try again." }]);
    } finally { setBusy(false); }
  }

  return <div className="chat-widget">
    {open && <section className="chat-panel">
      <header><strong>SmartEvent Assistant</strong><button onClick={() => setOpen(false)} aria-label="Close chat">×</button></header>
      <div className="chat-messages">{messages.map((m, i) => <p key={i} className={`chat-message ${m.from}`}>{m.text}</p>)}</div>
      <div className="chat-suggestions">
        {["Trending events", "Suggest music events", "Show my bookings"].map(s => <button key={s} onClick={() => send(s)}>{s}</button>)}
      </div>
      <form onSubmit={e => { e.preventDefault(); send(); }}><input value={message} onChange={e => setMessage(e.target.value)} placeholder="Ask about events..." maxLength={1000}/><button disabled={busy}>Send</button></form>
    </section>}
    <button className="chat-launcher" onClick={() => setOpen(v => !v)}>{open ? "Close chat" : "💬 Ask SmartEvent"}</button>
  </div>;
}
