import { useEffect, useState } from "react";
import axios from "axios";
const API = "http://127.0.0.1:8000/api/v1";
export default function Profile() {
  const [profile, setProfile] = useState({ username: "", location: "", profile_picture: "" });
  const [summary, setSummary] = useState(null); const [message, setMessage] = useState("");
  const headers = { Authorization: `Bearer ${localStorage.getItem("access_token")}` };
  useEffect(() => { axios.get(`${API}/profile/summary`, { headers }).then(r => { setSummary(r.data); setProfile({ username: r.data.user.username || "", location: r.data.user.location || "", profile_picture: r.data.user.profile_picture || "" }); }).catch(e => setMessage(e.response?.data?.detail || "Please log in to view your profile.")); }, []);
  async function save(e) { e.preventDefault(); try { const r = await axios.patch(`${API}/profile`, profile, { headers }); setProfile(p => ({ ...p, ...r.data })); setMessage("Profile updated successfully."); } catch (e) { setMessage(e.response?.data?.detail || "Unable to update profile."); } }
  return <main className="events-page profile-page"><h2>My Profile</h2>{message && <p>{message}</p>}<form className="profile-form" onSubmit={save}><label>Username<input value={profile.username} onChange={e => setProfile({...profile, username:e.target.value})} minLength="3" required /></label><label>Location<input value={profile.location} onChange={e => setProfile({...profile, location:e.target.value})} placeholder="City or area" /></label><label>Profile picture URL (optional)<input value={profile.profile_picture} onChange={e => setProfile({...profile, profile_picture:e.target.value})} /></label><button type="submit">Save Profile</button></form>{summary && <section className="profile-summary"><h3>Booking Summary</h3><p>Total bookings: {summary.booking_count}</p><p>Confirmed bookings: {summary.confirmed_bookings}</p><p>Tickets booked: {summary.tickets_booked}</p><p>Total spent: ₹{summary.total_spent}</p></section>}</main>;
}
