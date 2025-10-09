"""
Seed the database with synthetic hotel and room data
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def seed_hotels_and_rooms():
    """Insert synthetic data for 10 hotels with 5 rooms each"""
    db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/hotels"
    engine = create_engine(db_url)
    
    # Hotel data
    hotels_data = [
        {
            'name': 'Grand Plaza Hotel',
            'address': '123 Main Street',
            'city': 'New York',
            'state': 'NY',
            'zip_code': '10001',
            'phone': '(212) 555-0101',
            'email': 'info@grandplaza.com',
            'rating': 4.5,
            'amenities': ['WiFi', 'Pool', 'Gym', 'Restaurant', 'Spa'],
            'description': 'Luxury hotel in the heart of Manhattan with world-class amenities.'
        },
        {
            'name': 'Seaside Resort',
            'address': '456 Ocean Drive',
            'city': 'Miami',
            'state': 'FL',
            'zip_code': '33139',
            'phone': '(305) 555-0202',
            'email': 'reservations@seasideresort.com',
            'rating': 4.2,
            'amenities': ['WiFi', 'Beach Access', 'Pool', 'Restaurant', 'Bar'],
            'description': 'Beautiful beachfront resort with stunning ocean views.'
        },
        {
            'name': 'Mountain View Lodge',
            'address': '789 Alpine Way',
            'city': 'Denver',
            'state': 'CO',
            'zip_code': '80202',
            'phone': '(303) 555-0303',
            'email': 'stay@mountainviewlodge.com',
            'rating': 4.0,
            'amenities': ['WiFi', 'Fireplace', 'Hiking Trails', 'Restaurant'],
            'description': 'Cozy mountain lodge perfect for outdoor enthusiasts.'
        },
        {
            'name': 'Business Center Inn',
            'address': '321 Corporate Blvd',
            'city': 'Chicago',
            'state': 'IL',
            'zip_code': '60601',
            'phone': '(312) 555-0404',
            'email': 'bookings@businesscenter.com',
            'rating': 3.8,
            'amenities': ['WiFi', 'Business Center', 'Meeting Rooms', 'Gym'],
            'description': 'Modern hotel designed for business travelers.'
        },
        {
            'name': 'Historic Downtown Hotel',
            'address': '654 Heritage Street',
            'city': 'Boston',
            'state': 'MA',
            'zip_code': '02101',
            'phone': '(617) 555-0505',
            'email': 'welcome@historicdowntown.com',
            'rating': 4.3,
            'amenities': ['WiFi', 'Historic Tours', 'Restaurant', 'Bar'],
            'description': 'Charming historic hotel in downtown Boston.'
        },
        {
            'name': 'Desert Oasis Resort',
            'address': '987 Cactus Road',
            'city': 'Phoenix',
            'state': 'AZ',
            'zip_code': '85001',
            'phone': '(602) 555-0606',
            'email': 'info@desertoasis.com',
            'rating': 4.1,
            'amenities': ['WiFi', 'Pool', 'Spa', 'Golf Course', 'Restaurant'],
            'description': 'Luxurious desert resort with championship golf course.'
        },
        {
            'name': 'Lakefront Retreat',
            'address': '147 Lakeshore Drive',
            'city': 'Seattle',
            'state': 'WA',
            'zip_code': '98101',
            'phone': '(206) 555-0707',
            'email': 'stay@lakefrontretreat.com',
            'rating': 4.4,
            'amenities': ['WiFi', 'Lake Access', 'Kayak Rental', 'Restaurant'],
            'description': 'Peaceful lakefront hotel with water activities.'
        },
        {
            'name': 'City Center Suites',
            'address': '258 Downtown Plaza',
            'city': 'Atlanta',
            'state': 'GA',
            'zip_code': '30301',
            'phone': '(404) 555-0808',
            'email': 'reservations@citycentersuites.com',
            'rating': 3.9,
            'amenities': ['WiFi', 'Kitchenette', 'Gym', 'Business Center'],
            'description': 'Extended stay suites in the heart of Atlanta.'
        },
        {
            'name': 'Vineyard Inn',
            'address': '369 Wine Country Road',
            'city': 'Napa',
            'state': 'CA',
            'zip_code': '94558',
            'phone': '(707) 555-0909',
            'email': 'bookings@vineyardinn.com',
            'rating': 4.6,
            'amenities': ['WiFi', 'Wine Tasting', 'Restaurant', 'Spa'],
            'description': 'Boutique inn in the heart of wine country.'
        },
        {
            'name': 'Airport Express Hotel',
            'address': '741 Terminal Way',
            'city': 'Las Vegas',
            'state': 'NV',
            'zip_code': '89101',
            'phone': '(702) 555-1010',
            'email': 'info@airportexpress.com',
            'rating': 3.5,
            'amenities': ['WiFi', 'Airport Shuttle', 'Business Center'],
            'description': 'Convenient hotel with complimentary airport shuttle.'
        }
    ]
    
    # Room types and pricing
    room_types = [
        {'type': 'Standard King', 'base_price': 120, 'occupancy': 2},
        {'type': 'Standard Queen', 'base_price': 110, 'occupancy': 2},
        {'type': 'Deluxe Suite', 'base_price': 200, 'occupancy': 4},
        {'type': 'Executive Room', 'base_price': 160, 'occupancy': 2},
        {'type': 'Family Room', 'base_price': 180, 'occupancy': 6}
    ]
    
    with engine.connect() as conn:
        # Clear existing data
        conn.execute(text("DELETE FROM reservations"))
        conn.execute(text("DELETE FROM rooms"))
        conn.execute(text("DELETE FROM hotels"))
        
        # Insert hotels
        for i, hotel in enumerate(hotels_data, 1):
            conn.execute(text("""
                INSERT INTO hotels (id, name, address, city, state, zip_code, phone, email, rating, amenities, description)
                VALUES (:id, :name, :address, :city, :state, :zip_code, :phone, :email, :rating, :amenities, :description)
            """), {
                'id': i,
                'name': hotel['name'],
                'address': hotel['address'],
                'city': hotel['city'],
                'state': hotel['state'],
                'zip_code': hotel['zip_code'],
                'phone': hotel['phone'],
                'email': hotel['email'],
                'rating': hotel['rating'],
                'amenities': hotel['amenities'],
                'description': hotel['description']
            })
            
            # Insert 5 rooms for each hotel
            for j, room_type in enumerate(room_types, 1):
                # Vary pricing slightly by hotel rating
                price_multiplier = hotel['rating'] / 4.0
                price = round(room_type['base_price'] * price_multiplier, 2)
                
                room_amenities = ['WiFi', 'TV', 'Air Conditioning']
                if room_type['type'] in ['Deluxe Suite', 'Executive Room']:
                    room_amenities.extend(['Mini Bar', 'Coffee Maker'])
                if room_type['type'] == 'Family Room':
                    room_amenities.extend(['Sofa Bed', 'Microwave'])
                
                conn.execute(text("""
                    INSERT INTO rooms (hotel_id, room_number, room_type, price_per_night, max_occupancy, amenities)
                    VALUES (:hotel_id, :room_number, :room_type, :price_per_night, :max_occupancy, :amenities)
                """), {
                    'hotel_id': i,
                    'room_number': f"{i}0{j}",
                    'room_type': room_type['type'],
                    'price_per_night': price,
                    'max_occupancy': room_type['occupancy'],
                    'amenities': room_amenities
                })
        
        conn.commit()
        print("✅ Successfully seeded database with 10 hotels and 50 rooms")

if __name__ == "__main__":
    seed_hotels_and_rooms()