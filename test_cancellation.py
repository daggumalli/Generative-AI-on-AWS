"""
Test script for hotel reservation cancellation functionality
"""
import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.hotel_tools import cancel_reservation, get_reservation_details

load_dotenv()

def test_cancellation():
    """Test cancelling a reservation"""
    print("🧪 Testing Hotel Cancellation System")
    print("="*50)
    
    # Test 1: Look up existing reservations
    print("\n1. Looking up reservations for dag@gmail.com...")
    details_result = get_reservation_details(guest_email="dag@gmail.com")
    print(details_result)
    
    # Test 2: Try to cancel a reservation (you'll need to update the reservation_id)
    print("\n2. Attempting to cancel reservation...")
    print("Note: Update the reservation_id below based on the results above")
    
    # Example cancellation - update the reservation_id as needed
    cancellation_result = cancel_reservation(
        reservation_id=13,  # Update this with actual reservation ID
        guest_email="dag@gmail.com"
    )
    print(cancellation_result)

if __name__ == "__main__":
    test_cancellation()