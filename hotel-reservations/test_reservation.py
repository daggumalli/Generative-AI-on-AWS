"""
Test script for hotel reservation functionality
"""
import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.hotel_tools import make_reservation, get_available_rooms

load_dotenv()

def test_reservation():
    """Test making a reservation"""
    print("🧪 Testing Hotel Reservation System")
    print("="*50)
    
    # Test 1: Check available rooms
    print("\n1. Checking available rooms at hotel ID 1 for 2025-10-12 to 2025-10-14...")
    rooms_result = get_available_rooms(1, "2025-10-12", "2025-10-14")
    print(rooms_result)
    
    # Test 2: Make a reservation
    print("\n2. Making a test reservation...")
    reservation_result = make_reservation(
        room_id=2,  # Try room ID 2 (Standard Queen)
        guest_name="Srikanth D",
        guest_email="dag@gmail.com", 
        guest_phone="2923948923",
        check_in="2025-10-12",
        check_out="2025-10-14"
    )
    print(reservation_result)

if __name__ == "__main__":
    test_reservation()