import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import EventCard from "../components/EventCard";
import "../App.css";

function Home() {
  const navigate = useNavigate();
  const [recommendations, setRecommendations] = useState([]);
  const [trending, setTrending] = useState([]);
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) axios.get("http://127.0.0.1:8000/api/v1/recommendations", { headers: { Authorization: `Bearer ${token}` } })
      .then(r => { setRecommendations(r.data.recommended || []); setTrending(r.data.trending || []); }).catch(() => {});
    else axios.get("http://127.0.0.1:8000/api/v1/events?sort_by=popularity").then(r => setTrending(r.data || [])).catch(() => {});
  }, []);
  return <main>
    <section className="hero"><h2>Discover Amazing Events</h2><p>Find events, book tickets, get digital QR tickets, and stay updated with SmartEvent.</p><button onClick={() => navigate("/events")}>Explore Events</button></section>
    {recommendations.length > 0 && <section className="home-event-section"><h2>Recommended for You</h2><div className="events-container">{recommendations.slice(0,4).map(event => <EventCard key={event.id} event={event} />)}</div></section>}
    {trending.length > 0 && <section className="home-event-section"><h2>Trending Events</h2><div className="events-container">{trending.slice(0,4).map(event => <EventCard key={event.id} event={event} />)}</div></section>}
    <section className="features"><div><h3>🎫 Easy Booking</h3><p>Book your event tickets quickly and securely.</p></div><div><h3>📱 QR Tickets</h3><p>Get digital tickets with unique QR codes.</p></div><div><h3>🔔 Notifications</h3><p>Stay updated about your bookings and events.</p></div></section>
  </main>;
}
export default Home;
