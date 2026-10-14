# SmartEvent – Event Discovery & Ticket Booking System

<<<<<<< HEAD
## Project Overview

SmartEvent is a full-stack web application that allows users to discover events, book tickets, make simulated payments, apply discount coupons, receive notifications, and manage their digital tickets.

The application provides a simple interface for browsing events and managing bookings. It also includes event reviews, ticket verification, and event search and filtering.

## Technologies Used

### Backend
- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication
- Pydantic

### Frontend
- React
- Vite
- JavaScript
- CSS
- Axios

## Features

### 1. User Authentication
- User registration and login
- JWT-based authentication
- Protected routes for authenticated users

### 2. Event Discovery
- Browse available events
- View event details
- Search events by name
- Filter events by category, location, date, and ticket price
- Sort events by date, price, and popularity

### 3. Ticket Booking
- Select the number of tickets
- Apply coupon codes during booking
- View booking details and booking status
- Manage personal bookings

### 4. Payment System
- Simulated payment processing
- Support for successful and failed payment scenarios
- Transaction ID generation for successful payments
- Payment history
- Booking status updates after successful payment

**Note:** Payments are simulated for demonstration purposes. Real money is not processed.

### 5. Coupon Management
- Create and view coupons
- Percentage-based and fixed discounts
- Minimum booking amount validation
- Coupon expiry validation
- Usage limit and active-status validation

### 6. Event Reviews
- Submit ratings and written reviews
- View reviews for events
- Edit and delete personal reviews
- Validate booking eligibility before reviewing
- Display event ratings

### 7. Notifications
- Booking notifications
- Payment success and failure notifications
- View notification history
- Check unread notification count
- Mark individual notifications or all notifications as read

### 8. Digital Tickets
- Generate digital tickets for confirmed bookings
- View personal tickets
- Verify tickets using ticket codes

### 9. User Interface
- Responsive event cards
- Navigation between application pages
- Event details and booking pages
- Login and registration pages
- Booking and ticket history
- Payment confirmation and error feedback
=======
SmartEvent is a full-stack web application for discovering events and booking tickets online.

Users can register and log in, view available events, book tickets, manage their bookings, access digital tickets with QR codes, and verify tickets. The application also includes notifications and organizer features for managing events.

## Features

### User Authentication

* User registration
* User login
* JWT-based authentication
* Password hashing using bcrypt
* Protected API routes
* User profile
* Automatic authentication using a stored token

### Event Discovery

* View available events
* View individual event details
* Event information includes:

  * Event name
  * Date and time
  * Location
  * Category
  * Ticket price
  * Available tickets

### Ticket Booking

* Select the number of tickets
* Calculate total ticket price
* Confirm bookings
* View booking history
* Cancel confirmed bookings
* Prevent unauthorized users from accessing other users' bookings

### Digital Tickets

* Generate digital tickets for confirmed bookings
* Unique ticket code for every ticket
* QR code generation
* View digital tickets
* Download QR ticket
* Display ticket and booking information

### Ticket Verification

* Verify tickets using the unique ticket code
* Display ticket verification status
* Show booking ID and ticket information
* QR code can be used for ticket verification

### Notifications

* Booking confirmation notifications
* Booking cancellation notifications
* Notification unread count
* Mark notifications as read

### Organizer Features

* Organizer role support
* Organizer event management
* Protected organizer routes

## Technology Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* JWT Authentication
* bcrypt
* QRCode

### Frontend

* React
* Vite
* JavaScript
* Axios
* React Router
* CSS

### Development Tools

* Visual Studio Code
* Git
* GitHub
* Uvicorn
>>>>>>> origin/main

## Project Structure

```text
SmartEvent-FullStack-main/
<<<<<<< HEAD
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── config.py
│   ├── routers/
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── index.html
│
└── README.md
```

*Note: The structure above shows the main project files. Some additional files may be present in your local project.*

## Requirements

Install the following before running

## Phase 4 additions

Phase 4 adds the following API capabilities:

- `GET /api/v1/events/{event_id}/availability` and WebSocket `/api/v1/ws/events/{event_id}/availability`
- `POST /api/v1/events/{event_id}/view` and `GET /api/v1/recommendations`
- `GET /api/v1/wishlist`, `POST /api/v1/wishlist/{event_id}`, and `DELETE /api/v1/wishlist/{event_id}`
- `GET /api/v1/events/{event_id}/updates` and `POST /api/v1/events/{event_id}/updates`
- `PATCH /api/v1/profile` and `GET /api/v1/profile/summary`
- `POST /api/v1/chat` (JWT protected; provides event discovery and booking assistance using local matching rules)
- Event search supports category, search text, location, date range, minimum/maximum price, and popularity/price/date sorting.

The WebSocket sends availability updates after successful booking creation. The booking endpoint uses a conditional database update so concurrent requests cannot reserve more tickets than are available.

### Run locally

Backend:
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

Frontend (in another terminal):
```powershell
cd frontend
npm install
npm run dev
```

Open `http://127.0.0.1:8000/docs` for the API documentation and the Vite URL shown in the frontend terminal for the website.

**Important notes:** The chatbot is a local rule-based assistant, not a connected third-party generative AI model. To enable organizer/admin-only announcements, users need `role` set to `ADMIN` or `ORGANIZER` in the database; new registrations default to `USER`. The optional profile-picture field currently accepts a URL rather than uploading an image file. SQLite schema migration adds the Phase 4 user fields to existing databases on startup.
=======
│
├── backend/
│   ├── routers/
│   │   ├── auth.py
│   │   ├── bookings.py
│   │   ├── events.py
│   │   ├── notifications.py
│   │   ├── organizer.py
│   │   └── tickets.py
│   │
│   ├── static/
│   │   └── qrcodes/
│   │
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── database.py
│   ├── requirements.txt
│   ├── update_db.py
│   └── update_role.py
│
├── frontend/
│   └── ...
│
├── screenshots/
│   ├── Screenshot (236).png
│   ├── Screenshot (237).png
│   ├── Screenshot (238).png
│   ├── Screenshot (239).png
│   ├── Screenshot (240).png
│   ├── Screenshot (241).png
│   ├── Screenshot (242).png
│   ├── Screenshot (243).png
│   ├── Screenshot (244).png
│   └── Screenshot (245).png
│
├── .gitignore
└── README.md
```

## Backend Setup

Open PowerShell and go to the backend folder:

```powershell
cd "C:\Users\reddy\OneDrive\Desktop\SmartEvent-FullStack-main\backend"
```

Create a virtual environment:

```powershell
python -m venv venv
```

Activate the virtual environment:

```powershell
.\venv\Scripts\activate
```

Install the required packages:

```powershell
pip install -r requirements.txt
```

Start the FastAPI server:

```powershell
uvicorn main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Frontend Setup

Open another PowerShell terminal and go to the frontend folder:

```powershell
cd "C:\Users\reddy\OneDrive\Desktop\SmartEvent-FullStack-main\frontend"
```

Install frontend dependencies:

```powershell
npm install
```

Start the React development server:

```powershell
npm run dev
```

The frontend will normally run at:

```text
http://localhost:5173
```

## Application Flow

The main application flow is:

```text
Register
   ↓
Login
   ↓
View Events
   ↓
Select Event
   ↓
Book Tickets
   ↓
Booking Confirmation
   ↓
Generate Digital Ticket
   ↓
QR Code
   ↓
Verify Ticket
```

## API Endpoints

The backend API uses the `/api/v1` prefix.

### Authentication

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
```

### Events

```text
GET /api/v1/events
GET /api/v1/events/{event_id}
```

### Bookings

```text
POST /api/v1/bookings
GET /api/v1/bookings/my-bookings
GET /api/v1/bookings/{booking_id}
PATCH /api/v1/bookings/{booking_id}/cancel
```

### Tickets

```text
POST /api/v1/tickets/booking/{booking_id}
GET /api/v1/tickets/my-tickets
GET /api/v1/tickets/verify/{ticket_code}
```

### Notifications

```text
GET /api/v1/notifications
GET /api/v1/notifications/unread-count
PATCH /api/v1/notifications/{notification_id}/read
```

## Authentication

SmartEvent uses JWT tokens for authentication.

After login, the authentication token is stored on the frontend and automatically sent with protected API requests.

Protected features include:

* My Bookings
* My Tickets
* Ticket Verification
* Notifications
* Booking and cancellation operations

## Booking and Ticket System

When a user books an event, the system creates a booking with:

* Booking ID
* User ID
* Event ID
* Number of tickets
* Total amount
* Booking status
* Booking date

After a confi
>>>>>>> origin/main
