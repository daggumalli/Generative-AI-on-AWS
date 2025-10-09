"""
Test script for Hotel Reservations Agent
"""
import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from hotel_agent import HotelReservationAgent

def test_agent():
    """Test the hotel agent with sample queries"""
    print("🧪 Testing Hotel Reservations Agent")
    print("="*50)
    
    try:
        # Initialize agent
        agent = HotelReservationAgent()
        
        # Test queries
        test_queries = [
            "Search for hotels in New York",
            "Find hotels with rating above 4.0",
            "Show me available rooms at hotel ID 1 from 2025-03-15 to 2025-03-18",
            "What hotels are available in Miami?",
            "Help me understand how to make a reservation"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🔍 Test {i}: {query}")
            print("-" * 50)
            
            try:
                response = agent.chat(query)
                print(f"Response: {response}")
            except Exception as e:
                print(f"❌ Error: {str(e)}")
            
            print("\n" + "="*50)
        
        print("\n✅ Agent testing completed!")
        
    except Exception as e:
        print(f"❌ Failed to initialize agent: {str(e)}")
        print("Please ensure:")
        print("1. Database is running and configured")
        print("2. AWS credentials are set up")
        print("3. All dependencies are installed")

if __name__ == "__main__":
    load_dotenv()
    test_agent()