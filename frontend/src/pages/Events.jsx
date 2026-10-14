import { useEffect, useState } from "react";
import axios from "axios";
import "../App.css";

import EventCard from "../components/EventCard";

function Events() {
  const [events, setEvents] = useState([]);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [locationFilter, setLocationFilter] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [sortBy, setSortBy] = useState("date");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchEvents = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await axios.get(
        "http://127.0.0.1:8000/api/v1/events",
        {
          params: {
            search: search || undefined,
            category: category || undefined,
            location: locationFilter || undefined,
            start_date: startDate ? `${startDate}T00:00:00` : undefined,
            end_date: endDate ? `${endDate}T23:59:59` : undefined,
            sort_by: sortBy,
            min_price: minPrice === "" ? undefined : Number(minPrice),
            max_price: maxPrice === "" ? undefined : Number(maxPrice),
          },
        }
      );

      setEvents(response.data);
    } catch (error) {
      console.error(
        "Events error:",
        error
      );

      setError(
        "Unable to load events. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, [search, category, locationFilter, startDate, endDate, sortBy, minPrice, maxPrice]);

  return (
    <main className="events-page">

      <section className="events-header">

        <h2>
          Discover Events
        </h2>

        <p>
          Explore upcoming events and find
          something you love.
        </p>

        <div className="events-filters">

          <input
            type="text"
            placeholder="Search events..."
            value={search}
            onChange={(event) =>
              setSearch(event.target.value)
            }
          />

          <select
            value={category}
            onChange={(event) =>
              setCategory(event.target.value)
            }
          >

            <option value="">
              All Categories
            </option>

            <option value="Music">
              Music
            </option>

            <option value="Tech">
              Tech
            </option>

            <option value="Sports">
              Sports
            </option>

            <option value="Business">
              Business
            </option>

          </select>
          <input type="text" placeholder="Filter by location" value={locationFilter} onChange={event => setLocationFilter(event.target.value)} />
          <label className="date-filter">From <input type="date" value={startDate} onChange={event => setStartDate(event.target.value)} /></label>
          <label className="date-filter">To <input type="date" value={endDate} onChange={event => setEndDate(event.target.value)} /></label>
          <label className="date-filter">Min ₹<input type="number" min="0" value={minPrice} onChange={event => setMinPrice(event.target.value)} placeholder="0" /></label>
          <label className="date-filter">Max ₹<input type="number" min="0" value={maxPrice} onChange={event => setMaxPrice(event.target.value)} placeholder="Any" /></label>
          <select value={sortBy} onChange={event => setSortBy(event.target.value)} aria-label="Sort events"><option value="date">Sort: Date</option><option value="price">Sort: Price</option><option value="popularity">Sort: Popularity</option></select>

        </div>

      </section>

      {loading && (
        <p className="events-message">
          Loading events...
        </p>
      )}

      {error && (
        <p className="events-message error-message">
          {error}
        </p>
      )}

      {!loading &&
        !error &&
        events.length === 0 && (
          <p className="events-message">
            No events found.
          </p>
        )}

      {!loading &&
        !error &&
        events.length > 0 && (

          <section className="events-container">

            {events.map((event) => (
              <EventCard
                key={event.id}
                event={event}
              />
            ))}

          </section>

        )}

    </main>
  );
}

export default Events;