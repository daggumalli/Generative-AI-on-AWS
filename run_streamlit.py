"""
Script to run the Streamlit application with proper configuration
"""
import subprocess
import sys
import os
from dotenv import load_dotenv

def main():
    """Run the Streamlit application"""
    # Load environment variables
    load_dotenv()
    
    # Check if required environment variables are set
    required_vars = ['DB_HOST', 'DB_USER']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease update your .env file with the required database credentials.")
        return
    
    print("🏨 Starting Hotel Reservations Streamlit App...")
    print("📍 The app will be available at: http://localhost:8502")
    print("🔧 Press Ctrl+C to stop the application")
    print("-" * 60)
    
    try:
        # Run Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8502",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🏨 Hotel Reservations App stopped.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")
        print("Make sure Streamlit is installed: pip install streamlit")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()