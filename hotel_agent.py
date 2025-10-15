"""
Hotel Reservations Agent using AgentCore with Strands
"""
import os
import sys
from dotenv import load_dotenv
from strands import Agent
from strands.models import BedrockModel

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.hotel_tools import (
    search_hotels,
    get_available_rooms,
    make_reservation,
    get_reservation_details,
    cancel_reservation,
    web_search
)

load_dotenv()

class HotelReservationAgent:
    def __init__(self):
        self.setup_agent()
    
    def setup_agent(self):
        """Initialize the hotel reservation agent with tools and model"""
        
        # System prompt for the hotel agent
        SYSTEM_PROMPT = """You are a helpful and professional hotel reservation assistant.
        Your role is to:
        - Help customers search for hotels based on their preferences
        - Show available rooms for specific dates
        - Make hotel reservations with all required details
        - Retrieve and manage existing reservations
        - Cancel reservations when requested
        - Provide excellent customer service with a friendly, professional tone
        
        You have access to the following tools:
        1. search_hotels() - Search for hotels by location, rating, and price
        2. get_available_rooms() - Check room availability for specific dates
        3. make_reservation() - Create new hotel reservations
        4. get_reservation_details() - Look up existing reservations
        5. cancel_reservation() - Cancel existing reservations
        6. web_search() - Search the web for travel information, local attractions, restaurant recommendations, and general travel tips
        
        Always:
        - Ask for all required information before making reservations
        - Confirm details before finalizing bookings
        - Provide clear confirmation numbers and details
        - Be helpful with date formats (YYYY-MM-DD)
        - Suggest alternatives if requested options aren't available
        - Maintain a warm, professional tone throughout interactions
        
        For reservations, you need:
        - Guest name, email, and phone number
        - Check-in and check-out dates
        - Room preference (if any)
        
        Always use the appropriate tool to get accurate, real-time information from the database.
        
        Use web_search() when customers ask about:
        - Current date, time, or day of the week
        - Local attractions near hotels
        - Restaurant recommendations in the area
        - Transportation options
        - Weather information
        - Travel tips and guides
        - Things to do in specific cities
        - Current events or seasonal information
        
        Always prioritize using the hotel database tools first for hotel-specific queries, then supplement with web search for additional travel information."""
        
        # Initialize the Bedrock model (Claude 3.7 Sonnet)
        self.model = BedrockModel(
            model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            temperature=0.3,
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        
        # Create the agent with all hotel tools
        self.agent = Agent(
            model=self.model,
            tools=[
                search_hotels,
                get_available_rooms,
                make_reservation,
                get_reservation_details,
                cancel_reservation,
                web_search
            ],
            system_prompt=SYSTEM_PROMPT,
        )
        
        print("🏨 Hotel Reservation Agent initialized successfully!")
    
    def chat(self, message: str) -> str:
        """Process a user message and return the agent's response"""
        try:
            response = self.agent(message)
            return response
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}. Please try again or contact support."
    
    def run_interactive(self):
        """Run the agent in interactive mode"""
        print("\n" + "="*60)
        print("🏨 Welcome to Hotel Reservations Assistant!")
        print("="*60)
        print("I can help you:")
        print("• Search for hotels")
        print("• Check room availability")
        print("• Make reservations")
        print("• Look up existing bookings")
        print("• Cancel reservations")
        print("\nType 'quit' or 'exit' to end the conversation.")
        print("="*60 + "\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n🏨 Thank you for using Hotel Reservations Assistant! Have a great day!")
                    break
                
                if not user_input:
                    continue
                
                print("\nAgent: ", end="")
                response = self.chat(user_input)
                print(response)
                print("\n" + "-"*60 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n🏨 Thank you for using Hotel Reservations Assistant! Have a great day!")
                break
            except Exception as e:
                print(f"\nError: {str(e)}")
                print("Please try again.\n")

def main():
    """Main function to run the hotel reservation agent"""
    try:
        # Initialize the agent
        hotel_agent = HotelReservationAgent()
        
        # Run in interactive mode
        hotel_agent.run_interactive()
        
    except Exception as e:
        print(f"Failed to initialize Hotel Reservation Agent: {str(e)}")
        print("Please check your configuration and database connection.")

if __name__ == "__main__":
    main()