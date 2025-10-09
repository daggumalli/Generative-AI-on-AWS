"""
Hotel reservation tools for the AgentCore application
"""
from datetime import datetime, date
from typing import List, Dict, Optional
from strands.tools import tool
from database.models import db

@tool
def search_hotels(city: str = None, state: str = None, min_rating: float = None, max_price: float = None) -> str:
    """
    Search for hotels based on location and criteria.
    
    Args:
        city: City to search in (optional)
        state: State to search in (optional) 
        min_rating: Minimum hotel rating (1.0-5.0, optional)
        max_price: Maximum price per night (optional)
    
    Returns:
        Formatted list of matching hotels with details
    """
    try:
        query = """
            SELECT h.id, h.name, h.address, h.city, h.state, h.rating, h.amenities, h.description,
                   MIN(r.price_per_night) as min_price, MAX(r.price_per_night) as max_price
            FROM hotels h
            JOIN rooms r ON h.id = r.hotel_id
            WHERE 1=1
        """
        params = {}
        
        if city:
            query += " AND LOWER(h.city) = LOWER(:city)"
            params['city'] = city
            
        if state:
            query += " AND LOWER(h.state) = LOWER(:state)"
            params['state'] = state
            
        if min_rating:
            query += " AND h.rating >= :min_rating"
            params['min_rating'] = min_rating
            
        query += " GROUP BY h.id, h.name, h.address, h.city, h.state, h.rating, h.amenities, h.description"
        
        if max_price:
            query += " HAVING MIN(r.price_per_night) <= :max_price"
            params['max_price'] = max_price
            
        query += " ORDER BY h.rating DESC"
        
        hotels = db.execute_query(query, params)
        
        if not hotels:
            return "No hotels found matching your criteria."
        
        result = "🏨 Available Hotels:\n\n"
        for hotel in hotels:
            amenities_str = ", ".join(hotel['amenities']) if hotel['amenities'] else "None listed"
            result += f"**{hotel['name']}** (Rating: {hotel['rating']}/5.0)\n"
            result += f"📍 {hotel['address']}, {hotel['city']}, {hotel['state']}\n"
            result += f"💰 Price range: ${hotel['min_price']:.2f} - ${hotel['max_price']:.2f} per night\n"
            result += f"🎯 Amenities: {amenities_str}\n"
            result += f"📝 {hotel['description']}\n"
            result += f"🆔 Hotel ID: {hotel['id']}\n\n"
        
        return result
        
    except Exception as e:
        return f"Error searching hotels: {str(e)}"

@tool
def get_available_rooms(hotel_id: int, check_in: str, check_out: str) -> str:
    """
    Get available rooms for a specific hotel and date range.
    
    Args:
        hotel_id: Hotel ID to search rooms for
        check_in: Check-in date (YYYY-MM-DD format)
        check_out: Check-out date (YYYY-MM-DD format)
    
    Returns:
        Formatted list of available rooms with details
    """
    try:
        # Validate dates
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
        
        if check_in_date >= check_out_date:
            return "Error: Check-in date must be before check-out date."
        
        if check_in_date < date.today():
            return "Error: Check-in date cannot be in the past."
        
        # Get hotel info
        hotel_query = "SELECT name, city, state FROM hotels WHERE id = :hotel_id"
        hotel_info = db.execute_query(hotel_query, {'hotel_id': hotel_id})
        
        if not hotel_info:
            return f"Hotel with ID {hotel_id} not found."
        
        hotel = hotel_info[0]
        
        # Get available rooms (not booked during the requested period)
        rooms_query = """
            SELECT r.id, r.room_number, r.room_type, r.price_per_night, r.max_occupancy, r.amenities
            FROM rooms r
            WHERE r.hotel_id = :hotel_id 
            AND r.is_available = true
            AND r.id NOT IN (
                SELECT res.room_id 
                FROM reservations res 
                WHERE res.status = 'confirmed'
                AND (
                    (res.check_in_date <= :check_in AND res.check_out_date > :check_in)
                    OR (res.check_in_date < :check_out AND res.check_out_date >= :check_out)
                    OR (res.check_in_date >= :check_in AND res.check_out_date <= :check_out)
                )
            )
            ORDER BY r.price_per_night
        """
        
        rooms = db.execute_query(rooms_query, {
            'hotel_id': hotel_id,
            'check_in': check_in,
            'check_out': check_out
        })
        
        if not rooms:
            return f"No rooms available at {hotel['name']} for {check_in} to {check_out}."
        
        nights = (check_out_date - check_in_date).days
        
        result = f"🏨 Available Rooms at {hotel['name']}\n"
        result += f"📍 {hotel['city']}, {hotel['state']}\n"
        result += f"📅 {check_in} to {check_out} ({nights} nights)\n\n"
        
        for room in rooms:
            total_cost = room['price_per_night'] * nights
            amenities_str = ", ".join(room['amenities']) if room['amenities'] else "Standard amenities"
            
            result += f"**Room {room['room_number']}** - {room['room_type']}\n"
            result += f"💰 ${room['price_per_night']:.2f}/night (Total: ${total_cost:.2f})\n"
            result += f"👥 Max occupancy: {room['max_occupancy']} guests\n"
            result += f"🎯 Amenities: {amenities_str}\n"
            result += f"🆔 Room ID: {room['id']}\n\n"
        
        return result
        
    except ValueError:
        return "Error: Please use YYYY-MM-DD format for dates."
    except Exception as e:
        return f"Error getting available rooms: {str(e)}"

@tool
def make_reservation(room_id: int, guest_name: str, guest_email: str, guest_phone: str, 
                    check_in: str, check_out: str) -> str:
    """
    Make a hotel reservation.
    
    Args:
        room_id: Room ID to reserve
        guest_name: Guest's full name
        guest_email: Guest's email address
        guest_phone: Guest's phone number
        check_in: Check-in date (YYYY-MM-DD format)
        check_out: Check-out date (YYYY-MM-DD format)
    
    Returns:
        Confirmation details or error message
    """
    try:
        # Validate dates
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
        
        if check_in_date >= check_out_date:
            return "Error: Check-in date must be before check-out date."
        
        if check_in_date < date.today():
            return "Error: Check-in date cannot be in the past."
        
        # Get room and hotel details
        room_query = """
            SELECT r.id, r.room_number, r.room_type, r.price_per_night, r.hotel_id,
                   h.name as hotel_name, h.address, h.city, h.state, h.phone as hotel_phone
            FROM rooms r
            JOIN hotels h ON r.hotel_id = h.id
            WHERE r.id = :room_id AND r.is_available = true
        """
        
        room_info = db.execute_query(room_query, {'room_id': room_id})
        
        if not room_info:
            return f"Room with ID {room_id} not found or not available."
        
        room = room_info[0]
        
        # Check if room is available for the requested dates
        availability_query = """
            SELECT COUNT(*) as conflicts
            FROM reservations 
            WHERE room_id = :room_id 
            AND status = 'confirmed'
            AND (
                (check_in_date <= :check_in AND check_out_date > :check_in)
                OR (check_in_date < :check_out AND check_out_date >= :check_out)
                OR (check_in_date >= :check_in AND check_out_date <= :check_out)
            )
        """
        
        conflicts = db.execute_query(availability_query, {
            'room_id': room_id,
            'check_in': check_in,
            'check_out': check_out
        })
        
        if conflicts[0]['conflicts'] > 0:
            return f"Room {room['room_number']} is not available for the selected dates."
        
        # Calculate total amount
        nights = (check_out_date - check_in_date).days
        total_amount = room['price_per_night'] * nights
        
        # Create reservation
        reservation_query = """
            INSERT INTO reservations (room_id, guest_name, guest_email, guest_phone, 
                                    check_in_date, check_out_date, total_amount, status)
            VALUES (:room_id, :guest_name, :guest_email, :guest_phone, 
                    :check_in, :check_out, :total_amount, 'confirmed')
        """
        
        db.execute_query(reservation_query, {
            'room_id': room_id,
            'guest_name': guest_name,
            'guest_email': guest_email,
            'guest_phone': guest_phone,
            'check_in': check_in,
            'check_out': check_out,
            'total_amount': total_amount
        })
        
        # Get the reservation ID from the most recent insert for this guest
        reservation_id_query = """
            SELECT id FROM reservations 
            WHERE guest_email = :guest_email 
            ORDER BY created_at DESC LIMIT 1
        """
        reservation_result = db.execute_query(reservation_id_query, {'guest_email': guest_email})
        reservation_id = reservation_result[0]['id']
        
        # Return confirmation
        confirmation = f"✅ **Reservation Confirmed!**\n\n"
        confirmation += f"🆔 Reservation ID: {reservation_id}\n"
        confirmation += f"🏨 Hotel: {room['hotel_name']}\n"
        confirmation += f"📍 Address: {room['address']}, {room['city']}, {room['state']}\n"
        confirmation += f"🏠 Room: {room['room_number']} ({room['room_type']})\n"
        confirmation += f"👤 Guest: {guest_name}\n"
        confirmation += f"📧 Email: {guest_email}\n"
        confirmation += f"📞 Phone: {guest_phone}\n"
        confirmation += f"📅 Check-in: {check_in}\n"
        confirmation += f"📅 Check-out: {check_out}\n"
        confirmation += f"🌙 Nights: {nights}\n"
        confirmation += f"💰 Total Amount: ${total_amount:.2f}\n\n"
        confirmation += f"📞 Hotel Contact: {room['hotel_phone']}\n"
        confirmation += f"Please save this confirmation for your records."
        
        return confirmation
        
    except ValueError:
        return "Error: Please use YYYY-MM-DD format for dates."
    except Exception as e:
        return f"Error making reservation: {str(e)}"

@tool
def get_reservation_details(reservation_id: int = None, guest_email: str = None) -> str:
    """
    Get reservation details by reservation ID or guest email.
    
    Args:
        reservation_id: Reservation ID to look up (optional)
        guest_email: Guest email to search reservations (optional)
    
    Returns:
        Formatted reservation details
    """
    try:
        if not reservation_id and not guest_email:
            return "Error: Please provide either reservation ID or guest email."
        
        query = """
            SELECT res.id, res.guest_name, res.guest_email, res.guest_phone,
                   res.check_in_date, res.check_out_date, res.total_amount, res.status,
                   res.created_at, r.room_number, r.room_type,
                   h.name as hotel_name, h.address, h.city, h.state, h.phone as hotel_phone
            FROM reservations res
            JOIN rooms r ON res.room_id = r.id
            JOIN hotels h ON r.hotel_id = h.id
            WHERE 1=1
        """
        params = {}
        
        if reservation_id:
            query += " AND res.id = :reservation_id"
            params['reservation_id'] = reservation_id
        
        if guest_email:
            query += " AND LOWER(res.guest_email) = LOWER(:guest_email)"
            params['guest_email'] = guest_email
        
        query += " ORDER BY res.created_at DESC"
        
        reservations = db.execute_query(query, params)
        
        if not reservations:
            return "No reservations found matching your criteria."
        
        result = "🎫 **Reservation Details:**\n\n"
        
        for res in reservations:
            nights = (res['check_out_date'] - res['check_in_date']).days
            
            result += f"🆔 Reservation ID: {res['id']}\n"
            result += f"📊 Status: {res['status'].title()}\n"
            result += f"🏨 Hotel: {res['hotel_name']}\n"
            result += f"📍 Address: {res['address']}, {res['city']}, {res['state']}\n"
            result += f"🏠 Room: {res['room_number']} ({res['room_type']})\n"
            result += f"👤 Guest: {res['guest_name']}\n"
            result += f"📧 Email: {res['guest_email']}\n"
            result += f"📞 Phone: {res['guest_phone']}\n"
            result += f"📅 Check-in: {res['check_in_date']}\n"
            result += f"📅 Check-out: {res['check_out_date']}\n"
            result += f"🌙 Nights: {nights}\n"
            result += f"💰 Total Amount: ${res['total_amount']:.2f}\n"
            result += f"📞 Hotel Contact: {res['hotel_phone']}\n"
            result += f"📅 Booked on: {res['created_at'].strftime('%Y-%m-%d %H:%M')}\n\n"
        
        return result
        
    except Exception as e:
        return f"Error retrieving reservation details: {str(e)}"

@tool
def cancel_reservation(reservation_id: int, guest_email: str) -> str:
    """
    Cancel a hotel reservation.
    
    Args:
        reservation_id: Reservation ID to cancel
        guest_email: Guest email for verification
    
    Returns:
        Cancellation confirmation or error message
    """
    try:
        # Verify reservation exists and belongs to the guest
        verify_query = """
            SELECT res.id, res.guest_name, res.check_in_date, res.status,
                   h.name as hotel_name, r.room_number
            FROM reservations res
            JOIN rooms r ON res.room_id = r.id
            JOIN hotels h ON r.hotel_id = h.id
            WHERE res.id = :reservation_id 
            AND LOWER(res.guest_email) = LOWER(:guest_email)
        """
        
        reservation = db.execute_query(verify_query, {
            'reservation_id': reservation_id,
            'guest_email': guest_email
        })
        
        if not reservation:
            return "Reservation not found or email doesn't match."
        
        res = reservation[0]
        
        if res['status'] == 'cancelled':
            return f"Reservation {reservation_id} is already cancelled."
        
        # Check if cancellation is allowed (e.g., not same day)
        if res['check_in_date'] <= date.today():
            return "Cannot cancel reservations for today or past dates. Please contact the hotel directly."
        
        # Cancel the reservation
        cancel_query = """
            UPDATE reservations 
            SET status = 'cancelled' 
            WHERE id = :reservation_id
        """
        
        db.execute_query(cancel_query, {'reservation_id': reservation_id})
        
        result = f"✅ **Reservation Cancelled Successfully**\n\n"
        result += f"🆔 Reservation ID: {reservation_id}\n"
        result += f"🏨 Hotel: {res['hotel_name']}\n"
        result += f"🏠 Room: {res['room_number']}\n"
        result += f"👤 Guest: {res['guest_name']}\n"
        result += f"📅 Original Check-in: {res['check_in_date']}\n\n"
        result += f"Your reservation has been cancelled. "
        result += f"If you paid in advance, please allow 3-5 business days for refund processing."
        
        return result
        
    except Exception as e:
        return f"Error cancelling reservation: {str(e)}"