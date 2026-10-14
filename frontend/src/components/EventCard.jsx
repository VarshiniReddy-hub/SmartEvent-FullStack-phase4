import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function EventCard({ event }) {
  const navigate = useNavigate();
  const [saved, setSaved] = useState(false);
  const [saveMessage, setSaveMessage] = useState("");
  async function toggleWishlist() {
    const token = localStorage.getItem("access_token");
    if (!token) { setSaveMessage("Log in to save events"); return; }
    try {
      if (saved) await axios.delete(`http://127.0.0.1:8000/api/v1/wishlist/${event.id}`, { headers: { Authorization: `Bearer ${token}` } });
      else await axios.post(`http://127.0.0.1:8000/api/v1/wishlist/${event.id}`, {}, { headers: { Authorization: `Bearer ${token}` } });
      setSaved(!saved); setSaveMessage(saved ? "Removed" : "Saved");
    } catch (error) { setSaveMessage(error.response?.data?.detail || "Unable to save"); }
  }

  return (
    <div
      className="event-card"
    >

      <div className="event-image">
        🎫
      </div>

      <div className="event-content">

        <span className="event-category">
          {event.category}
        </span>

        <h3>
          {event.title}
        </h3>

        <p>
          {event.description}
        </p>

        <div className="event-details">

          <span>
            📍 {event.location}
          </span>

          <span>
            📅{" "}
            {new Date(
              event.event_date
            ).toLocaleDateString()}
          </span>

          <span>
            🎟️{" "}
            {event.available_tickets}{" "}
            tickets available
          </span>

        </div>

        <div className="event-bottom">

          <strong>
            ₹{event.ticket_price}
          </strong>

          <button onClick={() => navigate(`/events/${event.id}`)}>View Details</button>
          <button onClick={toggleWishlist} aria-label="Save event">{saved ? "♥ Saved" : "♡ Save"}</button>
          {saveMessage && <small>{saveMessage}</small>}

        </div>

      </div>

    </div>
  );
}

export default EventCard;