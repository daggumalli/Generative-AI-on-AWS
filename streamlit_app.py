"""
Hotel Reservations Agent - Streamlit Chat Interface
"""
import streamlit as st
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from hotel_agent import HotelReservationAgent

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="🏨 HG2 Hotel Reservations",
    page_icon="🏨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for chat interface
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .chat-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #fafafa;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #2196f3;
    }
    .agent-message {
        background-color: #f3e5f5;
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #9c27b0;
    }
    .system-status {
        font-size: 0.9rem;
        color: #666;
        text-align: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent' not in st.session_state:
    with st.spinner("🔧 Initializing Hotel Reservations Agent..."):
        try:
            st.session_state.agent = HotelReservationAgent()
            st.session_state.agent_initialized = True
            st.session_state.init_error = None
        except Exception as e:
            st.session_state.agent_initialized = False
            st.session_state.init_error = str(e)

if 'messages' not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "🏨 Welcome to Hotel Reservations! I'm your AI assistant. I can help you:\n\n• Search for hotels by location and preferences\n• Check room availability for specific dates\n• Make hotel reservations\n• Look up existing bookings\n• Cancel reservations\n\nHow can I assist you today?"
        }
    ]

def display_chat():
    """Display the main chat interface"""
    # Header
    st.markdown('''
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 class="main-header">🏨 HG2 Hotel Reservations</h1>
        <div style="color: #666; font-size: 1.1rem; font-weight: 300; margin-top: -0.5rem;">
            AI Powered
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # System status
    if not st.session_state.agent_initialized:
        st.error("❌ **Agent Initialization Failed**")
        st.error(f"**Error:** {st.session_state.get('init_error', 'Unknown error')}")
        st.info("💡 **Troubleshooting:**")
        st.info("• Check that PostgreSQL is running: `brew services start postgresql@15`")
        st.info("• Verify database connection in .env file")
        st.info("• Ensure AWS credentials are configured")
        return
    # No system status display needed
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about hotels, availability, reservations..."):
        # Add and display user message immediately
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Processing your request..."):
                try:
                    response = st.session_state.agent.chat(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"I apologize, but I encountered an error: {str(e)}\n\nPlease try again or contact support if the issue persists."
                    st.markdown(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

def display_sidebar():
    """Display sidebar with helpful information"""
    with st.sidebar:
        st.title("🏨 HG2 Assistant")
        
        # System status
        if st.session_state.agent_initialized:
            st.success("✅ Agent Ready")
        else:
            st.error("❌ Agent Error")
        
        # Quick examples
        st.markdown("### 💡 Try asking:")
        st.markdown("""
        **Hotel Services:**
        - "Find hotels in New York"
        - "Show me rooms at Grand Plaza Hotel from March 15-18"
        - "I want to make a reservation"
        - "Look up my booking for john@email.com"
        
        **Travel Information:**
        - "What are the best restaurants near Grand Plaza Hotel?"
        - "What attractions are near Miami Beach?"
        - "How's the weather in Denver this week?"
        - "What's the best way to get from airport to downtown?"
        """)
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = [
                {
                    "role": "assistant", 
                    "content": "🏨 Welcome back! How can I help you with hotel reservations today?"
                }
            ]
            st.rerun()
        
        # Sample hotels info
        st.markdown("### 🏨 Sample Hotels Available")
        st.markdown("""
        1. **Grand Plaza Hotel** (New York, NY)
        2. **Seaside Resort** (Miami, FL)  
        3. **Mountain View Lodge** (Denver, CO)
        4. **Business Center Inn** (Chicago, IL)
        5. **Vineyard Inn** (Napa, CA)
        
        *...and 5 more hotels across the US*
        """)
        
        st.markdown("---")
        st.markdown("**🔧 Need Help?**")
        st.markdown("Contact support if you encounter any issues.")

def main():
    """Main application function"""
    # Display sidebar
    display_sidebar()
    
    # Display main chat interface
    display_chat()

if __name__ == "__main__":
    main()