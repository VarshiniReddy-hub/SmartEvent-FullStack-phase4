import { useLocation, useNavigate } from "react-router-dom";
import "../App.css";

function BookingConfirmation() {
  const navigate = useNavigate();
  const location = useLocation();

  const booking = location.state?.booking;
  const payment = location.state?.payment;
  const paymentSucceeded = payment?.payment_status === "SUCCESS";

  if (!booking) {
    return (
      <main className="booking-confirmation-page">
        <div className="booking-confirmation-card">

          <div className="confirmation-icon">
            ⚠️
          </div>

          <h2>Booking Details Not Found</h2>

          <p>
            We couldn't find the booking information.
          </p>

          <button
            onClick={() => navigate("/bookings")}
          >
            Go to My Bookings
          </button>

        </div>
      </main>
    );
  }

  return (
    <main className="booking-confirmation-page">

      <div className="booking-confirmation-card">

        <div className="confirmation-icon">
          {paymentSucceeded ? "✓" : "!"}
        </div>

        <h2>{paymentSucceeded ? "Payment Successful!" : payment ? "Payment Failed" : "Booking Status"}</h2>

        <p className="confirmation-message">
          {paymentSucceeded ? "Your payment is complete and your tickets are confirmed." : payment ? "Your payment did not complete. You can retry payment from your booking." : "Here are your booking details."}
        </p>

        <div className="confirmation-details">

          <div className="confirmation-row">
            <span>Booking ID</span>
            <strong>#{booking.id}</strong>
          </div>

          <div className="confirmation-row">
            <span>Event ID</span>
            <strong>{booking.event_id}</strong>
          </div>

          <div className="confirmation-row">
            <span>Tickets</span>
            <strong>{booking.ticket_quantity}</strong>
          </div>

          <div className="confirmation-row"><span>Subtotal</span><strong>₹{Number(booking.total_price).toFixed(2)}</strong></div>
          <div className="confirmation-row"><span>Discount</span><strong>−₹{Number(booking.discount_amount || 0).toFixed(2)}</strong></div>
          <div className="confirmation-row"><span>Final Amount</span><strong>₹{Number(booking.final_amount ?? booking.total_price).toFixed(2)}</strong></div>
          {payment && <div className="confirmation-row"><span>Payment</span><strong>{payment.payment_status}</strong></div>}
          {payment?.transaction_id && <div className="confirmation-row"><span>Transaction ID</span><strong>{payment.transaction_id}</strong></div>}

          <div className="confirmation-row">
            <span>Status</span>
            <strong className="confirmation-status">
              {booking.booking_status}
            </strong>
          </div>

        </div>

        <div className="confirmation-actions">

          {!paymentSucceeded && payment && <button className="confirmation-primary-button" onClick={() => navigate(`/events/${booking.event_id}/book`)}>Try Again</button>}
          <button
            className="confirmation-primary-button"
            onClick={() => navigate("/bookings")}
          >
            View My Bookings
          </button>

          <button
            className="confirmation-secondary-button"
            onClick={() => navigate("/events")}
          >
            Explore More Events
          </button>

        </div>

      </div>

    </main>
  );
}

export default BookingConfirmation;