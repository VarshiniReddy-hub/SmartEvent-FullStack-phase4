import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import "../App.css";

function EventDetails() {
  const { eventId } = useParams();
  const navigate = useNavigate();

  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [reviewData, setReviewData] = useState({ average_rating: null, review_count: 0, reviews: [] });
  const [rating, setRating] = useState(5);
  const [reviewText, setReviewText] = useState("");
  const [reviewMessage, setReviewMessage] = useState("");
  const [eventUpdates, setEventUpdates] = useState([]);

  useEffect(() => {
    const fetchEvent = async () => {
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/api/v1/events/${eventId}`
        );

        setEvent(response.data);
        axios.get(`http://127.0.0.1:8000/api/v1/events/${eventId}/updates`).then(r => setEventUpdates(r.data)).catch(() => {});
        const token = localStorage.getItem("access_token");
        if (token) axios.post(`http://127.0.0.1:8000/api/v1/events/${eventId}/view`, {}, { headers: { Authorization: `Bearer ${token}` } }).catch(() => {});
        const reviewsResponse = await axios.get(`http://127.0.0.1:8000/api/v1/reviews/event/${eventId}`);
        setReviewData(reviewsResponse.data);
      } catch (error) {
        console.error("Event details error:", error);

        setError(
          "Unable to load event details."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchEvent();
  }, [eventId]);

  useEffect(() => {
    let socket;
    let interval;
    const refreshAvailability = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/v1/events/${eventId}/availability`);
        setEvent(old => old ? { ...old, available_tickets: response.data.available_tickets } : old);
      } catch (_) {}
    };
    socket = new WebSocket(`ws://127.0.0.1:8000/api/v1/ws/events/${eventId}/availability`);
    socket.onmessage = event => {
      try { const data = JSON.parse(event.data); setEvent(old => old ? { ...old, available_tickets: data.available_tickets } : old); } catch (_) {}
    };
    socket.onerror = () => { if (socket) socket.close(); };
    interval = setInterval(refreshAvailability, 10000);
    return () => { if (socket) socket.close(); clearInterval(interval); };
  }, [eventId]);

  if (loading) {
    return (
      <main className="event-details-page">
        <p>Loading event details...</p>
      </main>
    );
  }

  if (error) {
    return (
      <main className="event-details-page">
        <p>{error}</p>
      </main>
    );
  }

  if (!event) {
    return (
      <main className="event-details-page">
        <p>Event not found.</p>
      </main>
    );
  }

  const submitReview = async (event) => {
    event.preventDefault();
    const token = localStorage.getItem("access_token");
    try {
      await axios.post("http://127.0.0.1:8000/api/v1/reviews", { event_id: Number(eventId), rating: Number(rating), review_text: reviewText }, { headers: { Authorization: `Bearer ${token}` } });
      setReviewMessage("Thanks! Your review has been submitted."); setReviewText("");
      const response = await axios.get(`http://127.0.0.1:8000/api/v1/reviews/event/${eventId}`); setReviewData(response.data);
    } catch (err) { setReviewMessage(err.response?.data?.detail || "Unable to submit review."); }
  };

  return (
    <main className="event-details-page">

      <div className="event-details-card">

        <div className="event-details-image">
          🎫
        </div>

        <div className="event-details-content">

          <span className="event-category">
            {event.category}
          </span>

          <h2>{event.title}</h2>

          <p className="event-description">
            {event.description}
          </p>

          <div className="event-info">

            <p>
              📍 <strong>Location:</strong>{" "}
              {event.location}
            </p>

            <p>
              📅 <strong>Date:</strong>{" "}
              {new Date(
                event.event_date
              ).toLocaleDateString()}
            </p>

            <p>
              🕐 <strong>Time:</strong>{" "}
              {new Date(
                event.event_date
              ).toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit"
              })}
            </p>

            <p>
              🎟️ <strong>Available Tickets:</strong>{" "}
              {event.available_tickets}
            </p>

            <p>
              💰 <strong>Ticket Price:</strong>{" "}
              ₹{event.ticket_price}
            </p>

          </div>

          <div className="event-details-actions">

            <button
              onClick={() =>
                navigate("/events")
              }
            >
              Back to Events
            </button>

            <button
              onClick={() =>
                navigate(`/events/${event.id}/book`)
              }
              disabled={event.available_tickets === 0}
            >
              {event.available_tickets === 0
                ? "Sold Out"
                : "Book Ticket"}
            </button>

          </div>

        </div>

      </div>

      <section className="live-updates-section">
        <h2>Live Updates</h2>
        {eventUpdates.length === 0 ? <p>No announcements yet.</p> : eventUpdates.map(update => <article key={update.id} className={update.is_important ? "event-update important" : "event-update"}><strong>{update.is_important ? "📢 Important: " : ""}{update.message}</strong><small>{new Date(update.created_at).toLocaleString()}</small></article>)}
      </section>

      <section className="reviews-section">
        <h2>Event reviews</h2>
        <p className="review-average">{reviewData.average_rating ? `★ ${reviewData.average_rating} / 5` : "Not rated yet"} · {reviewData.review_count} review(s)</p>
        {reviewData.reviews.map(review => <article className="review-card" key={review.id}><strong>{"★".repeat(review.rating)}{"☆".repeat(5-review.rating)}</strong><p>{review.review_text || "No written comment."}</p><small>{new Date(review.created_at).toLocaleDateString()}</small></article>)}
        <form className="review-form" onSubmit={submitReview}><h3>Leave a review</h3><label htmlFor="review-rating">Your rating</label><select id="review-rating" value={rating} onChange={e => setRating(Number(e.target.value))}>{[5,4,3,2,1].map(value => <option value={value} key={value}>{value} star{value > 1 ? "s" : ""}</option>)}</select><textarea value={reviewText} onChange={e => setReviewText(e.target.value)} maxLength={2000} placeholder="Share your experience (after attending the event)" /><button type="submit">Submit review</button>{reviewMessage && <p>{reviewMessage}</p>}</form>
      </section>

    </main>
  );
}

export default EventDetails;