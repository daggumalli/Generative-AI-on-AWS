# HG2 Hotel Reservations - Data Model Diagram

## 🗄️ **Entity Relationship Diagram (ERD)**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            HG2 HOTEL RESERVATIONS                              │
│                              DATA MODEL                                        │
└─────────────────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────────────────────────────┐
                    │                HOTELS                   │
                    │─────────────────────────────────────────│
                    │ 🔑 id: SERIAL PRIMARY KEY              │
                    │ 📝 name: VARCHAR(255) NOT NULL         │
                    │ 📍 address: VARCHAR(500) NOT NULL      │
                    │ 🏙️ city: VARCHAR(100) NOT NULL         │
                    │ 🗺️ state: VARCHAR(50) NOT NULL          │
                    │ 📮 zip_code: VARCHAR(20) NOT NULL       │
                    │ ☎️ phone: VARCHAR(20) NOT NULL          │
                    │ 📧 email: VARCHAR(255) NOT NULL        │
                    │ ⭐ rating: NUMERIC(2,1)                │
                    │    CHECK (rating >= 1.0 AND <= 5.0)   │
                    │ 🎯 amenities: TEXT[]                   │
                    │ 📄 description: TEXT                   │
                    │ 📅 created_at: TIMESTAMP DEFAULT NOW   │
                    └─────────────────┬───────────────────────┘
                                      │
                                      │ 1:N Relationship
                                      │ (One Hotel has Many Rooms)
                                      │
                    ┌─────────────────▼───────────────────────┐
                    │                ROOMS                    │
                    │─────────────────────────────────────────│
                    │ 🔑 id: SERIAL PRIMARY KEY              │
                    │ 🔗 hotel_id: INTEGER FK → hotels(id)   │
                    │    ON DELETE CASCADE                    │
                    │ 🚪 room_number: VARCHAR(10) NOT NULL   │
                    │ 🏠 room_type: VARCHAR(50) NOT NULL     │
                    │ 💰 price_per_night: NUMERIC(10,2)      │
                    │ 👥 max_occupancy: INTEGER NOT NULL     │
                    │ 🎯 amenities: TEXT[]                   │
                    │ ✅ is_available: BOOLEAN DEFAULT TRUE  │
                    │ 📅 created_at: TIMESTAMP DEFAULT NOW   │
                    │                                         │
                    │ 🔒 UNIQUE(hotel_id, room_number)       │
                    └─────────────────┬───────────────────────┘
                                      │
                                      │ 1:N Relationship
                                      │ (One Room has Many Reservations)
                                      │
                    ┌─────────────────▼───────────────────────┐
                    │            RESERVATIONS                 │
                    │─────────────────────────────────────────│
                    │ 🔑 id: SERIAL PRIMARY KEY              │
                    │ 🔗 room_id: INTEGER FK → rooms(id)     │
                    │    ON DELETE CASCADE                    │
                    │ 👤 guest_name: VARCHAR(255) NOT NULL   │
                    │ 📧 guest_email: VARCHAR(255) NOT NULL  │
                    │ ☎️ guest_phone: VARCHAR(20)            │
                    │ 📅 check_in_date: DATE NOT NULL        │
                    │ 📅 check_out_date: DATE NOT NULL       │
                    │ 💵 total_amount: NUMERIC(10,2)         │
                    │ 📊 status: VARCHAR(20)                 │
                    │    DEFAULT 'confirmed'                  │
                    │ 📅 created_at: TIMESTAMP DEFAULT NOW   │
                    │                                         │
                    │ 🔒 CHECK (check_out_date >             │
                    │           check_in_date)                │
                    └─────────────────────────────────────────┘
```

## 🔗 **Relationship Details**

### **HOTELS → ROOMS (1:N)**
```
┌─────────────┐         ┌─────────────┐
│   HOTELS    │ 1     N │    ROOMS    │
│             │◄────────│             │
│ id (PK)     │         │ hotel_id(FK)│
└─────────────┘         └─────────────┘

• One hotel can have multiple rooms
• Each room belongs to exactly one hotel
• CASCADE DELETE: Deleting hotel removes all its rooms
```

### **ROOMS → RESERVATIONS (1:N)**
```
┌─────────────┐         ┌─────────────┐
│    ROOMS    │ 1     N │RESERVATIONS │
│             │◄────────│             │
│ id (PK)     │         │ room_id(FK) │
└─────────────┘         └─────────────┘

• One room can have multiple reservations (over time)
• Each reservation is for exactly one room
• CASCADE DELETE: Deleting room removes all its reservations
```

## 📊 **Data Types & Constraints**

### **Primary Keys**
```sql
hotels.id        → SERIAL (Auto-increment integer)
rooms.id         → SERIAL (Auto-increment integer)  
reservations.id  → SERIAL (Auto-increment integer)
```

### **Foreign Keys**
```sql
rooms.hotel_id        → REFERENCES hotels(id) ON DELETE CASCADE
reservations.room_id  → REFERENCES rooms(id) ON DELETE CASCADE
```

### **Unique Constraints**
```sql
rooms: UNIQUE(hotel_id, room_number)  -- No duplicate room numbers per hotel
```

### **Check Constraints**
```sql
hotels.rating: CHECK (rating >= 1.0 AND rating <= 5.0)
reservations: CHECK (check_out_date > check_in_date)
```

### **Array Fields**
```sql
hotels.amenities[]     → ['WiFi', 'Pool', 'Gym', 'Restaurant']
rooms.amenities[]      → ['WiFi', 'TV', 'Air Conditioning', 'Mini Bar']
```

## 🎯 **Business Rules**

### **Hotel Rules**
- ✅ Each hotel must have unique name per city
- ✅ Rating must be between 1.0 and 5.0
- ✅ Contact information (phone, email) required
- ✅ Amenities stored as PostgreSQL array

### **Room Rules**
- ✅ Room numbers must be unique within each hotel
- ✅ Price must be positive decimal (10,2 precision)
- ✅ Max occupancy must be positive integer
- ✅ Rooms can be marked as unavailable

### **Reservation Rules**
- ✅ Check-out date must be after check-in date
- ✅ Guest email required for communication
- ✅ Total amount calculated from room price × nights
- ✅ Status defaults to 'confirmed'

## 📈 **Sample Data Structure**

### **Hotels Sample**
```sql
INSERT INTO hotels VALUES (
    1,                                    -- id
    'Grand Plaza Hotel',                  -- name
    '123 Main Street',                    -- address
    'New York',                           -- city
    'NY',                                 -- state
    '10001',                             -- zip_code
    '(212) 555-0101',                    -- phone
    'info@grandplaza.com',               -- email
    4.5,                                 -- rating
    ARRAY['WiFi','Pool','Gym','Spa'],    -- amenities
    'Luxury hotel in Manhattan',         -- description
    NOW()                                -- created_at
);
```

### **Rooms Sample**
```sql
INSERT INTO rooms VALUES (
    1,                                    -- id
    1,                                    -- hotel_id (FK)
    '101',                               -- room_number
    'Standard King',                     -- room_type
    135.00,                              -- price_per_night
    2,                                   -- max_occupancy
    ARRAY['WiFi','TV','AC'],             -- amenities
    true,                                -- is_available
    NOW()                                -- created_at
);
```

### **Reservations Sample**
```sql
INSERT INTO reservations VALUES (
    1,                                    -- id
    1,                                    -- room_id (FK)
    'John Smith',                        -- guest_name
    'john@email.com',                    -- guest_email
    '555-123-4567',                      -- guest_phone
    '2025-10-15',                        -- check_in_date
    '2025-10-17',                        -- check_out_date
    270.00,                              -- total_amount (135 × 2 nights)
    'confirmed',                         -- status
    NOW()                                -- created_at
);
```

## 🔍 **Query Patterns**

### **Find Hotels in City**
```sql
SELECT * FROM hotels 
WHERE LOWER(city) = LOWER('New York')
ORDER BY rating DESC;
```

### **Get Available Rooms**
```sql
SELECT r.*, h.name as hotel_name
FROM rooms r
JOIN hotels h ON r.hotel_id = h.id
WHERE r.hotel_id = 1 
  AND r.is_available = true
  AND r.id NOT IN (
    SELECT room_id FROM reservations 
    WHERE status = 'confirmed'
    AND check_in_date <= '2025-10-17'
    AND check_out_date > '2025-10-15'
  );
```

### **Get Reservation Details**
```sql
SELECT res.*, r.room_number, r.room_type, h.name as hotel_name
FROM reservations res
JOIN rooms r ON res.room_id = r.id
JOIN hotels h ON r.hotel_id = h.id
WHERE res.guest_email = 'john@email.com';
```

## 📊 **Database Statistics**

### **Current Data Volume**
- **Hotels**: 10 records
- **Rooms**: 50 records (5 per hotel)
- **Reservations**: Variable (based on bookings)

### **Storage Estimates**
- **Hotels**: ~2KB per record
- **Rooms**: ~1KB per record
- **Reservations**: ~500B per record

### **Index Strategy**
```sql
-- Primary Keys (automatic)
CREATE INDEX hotels_pkey ON hotels(id);
CREATE INDEX rooms_pkey ON rooms(id);
CREATE INDEX reservations_pkey ON reservations(id);

-- Foreign Keys (automatic)
CREATE INDEX rooms_hotel_id_idx ON rooms(hotel_id);
CREATE INDEX reservations_room_id_idx ON reservations(room_id);

-- Business Queries
CREATE INDEX hotels_city_idx ON hotels(city);
CREATE INDEX hotels_rating_idx ON hotels(rating);
CREATE INDEX reservations_guest_email_idx ON reservations(guest_email);
CREATE INDEX reservations_dates_idx ON reservations(check_in_date, check_out_date);
```

## 🔄 **Data Lifecycle**

### **Hotel Lifecycle**
```
Create → Update Details → Add Rooms → Manage Availability → Archive
```

### **Room Lifecycle**
```
Create → Set Available → Book → Occupy → Clean → Available
```

### **Reservation Lifecycle**
```
Create → Confirm → Check-in → Check-out → Complete → Archive
```

This data model provides a solid foundation for the hotel reservations system with proper relationships, constraints, and scalability considerations.