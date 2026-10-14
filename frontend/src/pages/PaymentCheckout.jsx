import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";
import "../App.css";

function PaymentCheckout() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const booking = state?.booking;
  const event = state?.event;
  const [method, setMethod] = useState("UPI");
  const [result, setResult] = useState("SUCCESS");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  if (!booking) return <main className="payment-page"><section className="payment-card"><h2>Booking not found</h2><p>Please start from an event booking page.</p><button onClick={() => navigate("/events")}>Browse events</button></section></main>;

  const pay = async () => {
    const token = localStorage.getItem("access_token");
    try {
      setLoading(true); setError("");
      const response = await axios.post("http://127.0.0.1:8000/api/v1/payments/checkout", { booking_id: booking.id, payment_method: method, simulated_result: result }, { headers: { Authorization: `Bearer ${token}` } });
      navigate("/booking-confirmation", { state: { booking: { ...booking, booking_status: response.data.payment_status === "SUCCESS" ? "CONFIRMED" : "PENDING" }, payment: response.data, event } });
    } catch (err) { setError(err.response?.data?.detail || "Unable to process payment."); } finally { setLoading(false); }
  };

  return <main className="payment-page"><section className="payment-card">
    <span className="event-category">SECURE CHECKOUT · DEMO MODE</span><h2>Complete your payment</h2><p className="payment-muted">Review your booking before continuing.</p>
    <div className="payment-summary"><h3>{event?.title || `Event #${booking.event_id}`}</h3><p>Booking ID: #{booking.id}</p><p>Tickets: {booking.ticket_quantity}</p><p>Subtotal: ₹{Number(booking.total_price).toFixed(2)}</p><p>Discount: −₹{Number(booking.discount_amount || 0).toFixed(2)}</p><div className="payment-final"><span>Total to pay</span><strong>₹{Number(booking.final_amount ?? booking.total_price).toFixed(2)}</strong></div></div>
    <label htmlFor="payment-method">Payment method</label><select id="payment-method" value={method} onChange={e => setMethod(e.target.value)}><option value="UPI">UPI</option><option value="CARD">Card (simulated)</option><option value="NET_BANKING">Net banking (simulated)</option><option value="SIMULATED">Demo payment</option></select>
    <label htmlFor="payment-result">Test result</label><select id="payment-result" value={result} onChange={e => setResult(e.target.value)}><option value="SUCCESS">Simulate success</option><option value="FAILED">Simulate failure</option></select><p className="payment-muted">This is a test simulation. No real money will be charged.</p>
    {error && <p className="booking-error">{error}</p>}<button className="confirmation-primary-button" disabled={loading} onClick={pay}>{loading ? "Processing..." : `Pay ₹${Number(booking.final_amount ?? booking.total_price).toFixed(2)}`}</button><button className="confirmation-secondary-button" onClick={() => navigate("/bookings")}>Cancel checkout</button>
  </section></main>;
}
export default PaymentCheckout;
