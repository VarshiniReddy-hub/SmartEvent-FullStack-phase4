import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
const API = "http://127.0.0.1:8000/api/v1";
export default function Wishlist() {
  const [events, setEvents] = useState([]); const [error, setError] = useState(""); const navigate = useNavigate();
  async function load() { try { const r = await axios.get(`${API}/wishlist`, { headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` } }); setEvents(r.data); } catch (e) { setError(e.response?.data?.detail || "Unable to load wishlist."); } }
  useEffect(() => { load(); }, []);
  async function remove(id) { try { await axios.delete(`${API}/wishlist/${id}`, { headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` } }); load(); } catch (e) { setError("Unable to remove event."); } }
  return <main className="events-page"><h2>My Wishlist</h2>{error && <p>{error}</p>}{events.length === 0 && !error && <p>No saved events yet. Browse events and save your favourites.</p>}<section className="events-container">{events.map(e => <article className="event-card" key={e.id}><div className="event-content"><span>{e.category}</span><h3>{e.title}</h3><p>{e.location} · {new Date(e.event_date).toLocaleString()}</p><p>₹{e.ticket_price} · {e.available_tickets} tickets left</p><button onClick={() => navigate(`/events/${e.id}`)}>View event</button> <button onClick={() => remove(e.id)}>Remove</button></div></article>)}</section></main>;
}
