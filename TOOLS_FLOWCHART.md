# HG2 Hotel Reservations - Tools Flowchart

## 🔧 **Agent Tools Flow Diagram**

```
                                    ┌─────────────────────────────────┐
                                    │         USER INPUT              │
                                    │    "Find hotels in NYC"        │
                                    │    "Book a room"               │
                                    │    "Cancel reservation"        │
                                    └─────────────┬───────────────────┘
                                                  │
                                    ┌─────────────▼───────────────────┐
                                    │      STRANDS AGENT              │
                                    │   (Claude 3.7 Sonnet)          │
                                    │                                 │
                                    │  • Analyzes user intent         │
                                    │  • Selects appropriate tool     │
                                    │  • Formats response             │
                                    └─────────────┬───────────────────┘
                                                  │
                                                  │ Tool Selection
                                                  │
                        ┌─────────────────────────┼─────────────────────────┐
                        │                         │                         │
                        ▼                         ▼                         ▼
            ┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
            │   HOTEL SEARCH      │   │   RESERVATION       │   │   EXTERNAL INFO     │
            │      TOOLS          │   │      TOOLS          │   │      TOOLS          │
            └─────────────────────┘   └─────────────────────┘   └─────────────────────┘
                        │                         │                         │
                        │                         │                         │
        ┌───────────────┼───────────────┐  ┌─────┼─────────┐   ┌───────────┼───────────┐
        │               │               │  ┌─────┼─────┐ ┌─────┼─────┐ │           │           │
        ▼               ▼               ▼  ▼     ▼     ▼ ▼     ▼     ▼ ▼           ▼           ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│search_hotels│ │get_available│ │make_        │ │get_reservation│ │cancel_      │ │ web_search  │ │   Future    │
│             │ │   _rooms    │ │reservation  │ │   _details  │ │reservation  │ │             │ │   Tools     │
│             │ │             │ │             │ │             │ │             │ │             │ │             │
│ INPUT:      │ │ INPUT:      │ │ INPUT:      │ │ INPUT:      │ │ INPUT:      │ │ INPUT:      │ │             │
│ • city      │ │ • hotel_id  │ │ • room_id   │ │ • reservation_id│ │ • reservation_id│ │ • keywords  │ │             │
│ • state     │ │ • check_in  │ │ • guest_name│ │ • guest_email│ │ • guest_email│ │ • region    │ │             │
│ • rating    │ │ • check_out │ │ • guest_email│ │             │ │             │ │ • max_results│ │             │
│ • max_price │ │             │ │ • guest_phone│ │ OUTPUT:     │ │ OUTPUT:     │ │             │ │             │
│             │ │ OUTPUT:     │ │ • check_in  │ │ • booking   │ │ • cancellation│ │ OUTPUT:     │ │             │
│ OUTPUT:     │ │ • room list │ │ • check_out │ │   details   │ │   confirmation│ │ • search    │ │             │
│ • hotel list│ │ • pricing   │ │             │ │ • hotel info│ │             │ │   results   │ │             │
│ • details   │ │ • availability│ │ OUTPUT:   │ │ • guest info│ │             │ │ • links     │ │             │
│             │ │             │ │ • confirmation│ │             │ │             │ │             │ │             │
│             │ │             │ │ • reservation_id│ │           │ │             │ │             │ │             │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
        │               │       │             │ │             │               │
        │               │       │             │ │             │               │
        ▼               ▼       ▼             ▼ ▼             ▼               ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           DATABASE LAYER                                       │
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────────────────┐   │
│  │   HOTELS    │    │    ROOMS    │    │         RESERVATIONS            │   │
│  │   TABLE     │    │    TABLE    │    │            TABLE                │   │
│  │             │    │             │    │                                 │   │
│  │ ┌─────────┐ │    │ ┌─────────┐ │    │ ┌─────────────────────────────┐ │   │
│  │ │ Query   │ │    │ │ Query   │ │    │ │ Query                       │ │   │
│  │ │ Hotels  │◄┼────┼►│ Rooms   │ │    │ │ Reservations                │ │   │
│  │ │ by City │ │    │ │ by Hotel│ │    │ │ by Guest/ID                 │ │   │
│  │ └─────────┘ │    │ └─────────┘ │    │ └─────────────────────────────┘ │   │
│  └─────────────┘    └─────────────┘    └─────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  │
                                                  │
                                                  ▼
                                    ┌─────────────────────────────────┐
                                    │      EXTERNAL SERVICES          │
                                    │                                 │
                                    │  ┌─────────────────────────┐   │
                                    │  │    DuckDuckGo Search    │   │
                                    │  │                         │   │
                                    │  │ • Travel information    │   │
                                    │  │ • Local attractions     │   │
                                    │  │ • Restaurant reviews    │   │
                                    │  │ • Weather data          │   │
                                    │  │ • Transportation info   │   │
                                    │  └─────────────────────────┘   │
                                    └─────────────────────────────────┘
                                                  │
                                                  ▼
                                    ┌─────────────────────────────────┐
                                    │       RESPONSE FLOW             │
                                    │                                 │
                                    │  Tool Result → Agent → User     │
                                    │                                 │
                                    │ • Formatted response            │
                                    │ • Natural language              │
                                    │ • Actionable information        │
                                    │ • Follow-up suggestions         │
                                    └─────────────────────────────────┘
```

## 🔄 **Tool Decision Flow**

```
User Query → Intent Analysis → Tool Selection

┌─────────────────────────────────────────────────────────────────────────────────┐
│                            INTENT CLASSIFICATION                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  "Find hotels in NYC"           → search_hotels()                              │
│  "Show rooms at Grand Plaza"    → get_available_rooms()                        │
│  "Book room 101"                → make_reservation()                           │
│  "Look up my booking"           → get_reservation_details()                    │
│  "Cancel reservation 123"       → cancel_reservation()                        │
│  "What's the weather in Miami?" → web_search()                                │
│  "Best restaurants near hotel"  → web_search()                                │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🎯 **Tool Interaction Matrix**

```
┌─────────────────┬─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│     TOOL        │   HOTELS    │    ROOMS    │ RESERVATIONS│  EXTERNAL   │   OUTPUT    │
├─────────────────┼─────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ search_hotels   │     ✅      │     ✅      │      ❌     │      ❌     │ Hotel List  │
│ get_available   │     ✅      │     ✅      │      ✅     │      ❌     │ Room List   │
│ make_reservation│     ✅      │     ✅      │      ✅     │      ❌     │ Confirmation│
│ get_details     │     ✅      │     ✅      │      ✅     │      ❌     │ Booking Info│
│ cancel_res      │     ❌      │     ❌      │      ✅     │      ❌     │ Cancel Conf │
│ web_search      │     ❌      │     ❌      │      ❌     │      ✅     │ Search Results│
└─────────────────┴─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```

## 📊 **Database Schema Summary**

### **HOTELS Table**
```sql
CREATE TABLE hotels (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(500) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code VARCHAR(20) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL,
    rating NUMERIC(2,1) CHECK (rating >= 1.0 AND rating <= 5.0),
    amenities TEXT[],
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **ROOMS Table**
```sql
CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER REFERENCES hotels(id) ON DELETE CASCADE,
    room_number VARCHAR(10) NOT NULL,
    room_type VARCHAR(50) NOT NULL,
    price_per_night NUMERIC(10,2) NOT NULL,
    max_occupancy INTEGER NOT NULL,
    amenities TEXT[],
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(hotel_id, room_number)
);
```

### **RESERVATIONS Table**
```sql
CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    room_id INTEGER REFERENCES rooms(id) ON DELETE CASCADE,
    guest_name VARCHAR(255) NOT NULL,
    guest_email VARCHAR(255) NOT NULL,
    guest_phone VARCHAR(20),
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    total_amount NUMERIC(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'confirmed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (check_out_date > check_in_date)
);
```

## 🔗 **Relationships**
- Hotels → Rooms (1:Many)
- Rooms → Reservations (1:Many)
- Cascade deletes maintain referential integrity