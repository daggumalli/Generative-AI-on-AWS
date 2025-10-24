"""
Setup script for Hotel Reservations application
"""
import os
import sys
import subprocess
from dotenv import load_dotenv

def install_postgresql():
    """Install PostgreSQL using Homebrew on macOS"""
    print("🔧 Installing PostgreSQL...")
    try:
        # Check if Homebrew is installed
        subprocess.run(["brew", "--version"], check=True, capture_output=True)
        
        # Install PostgreSQL
        subprocess.run(["brew", "install", "postgresql@15"], check=True)
        
        # Start PostgreSQL service
        subprocess.run(["brew", "services", "start", "postgresql@15"], check=True)
        
        print("✅ PostgreSQL installed and started successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install PostgreSQL with Homebrew")
        print("Please install PostgreSQL manually:")
        print("1. Install Homebrew: https://brew.sh/")
        print("2. Run: brew install postgresql@15")
        print("3. Run: brew services start postgresql@15")
        return False
    except FileNotFoundError:
        print("❌ Homebrew not found")
        print("Please install Homebrew first: https://brew.sh/")
        return False

def setup_database():
    """Set up the database and tables"""
    print("🗄️ Setting up database...")
    try:
        from database.setup import create_database, create_tables
        create_database()
        create_tables()
        print("✅ Database setup completed!")
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {str(e)}")
        return False

def seed_database():
    """Seed the database with sample data"""
    print("🌱 Seeding database with sample data...")
    try:
        from database.seed_data import seed_hotels_and_rooms
        seed_hotels_and_rooms()
        print("✅ Database seeded successfully!")
        return True
    except Exception as e:
        print(f"❌ Database seeding failed: {str(e)}")
        return False

def install_python_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Python dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Python dependencies: {str(e)}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        print("📝 Creating .env file...")
        with open('.env', 'w') as f:
            f.write("""# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=hotels
DB_USER=postgres
DB_PASSWORD=

# AWS Configuration
AWS_REGION=us-east-1
AWS_PROFILE=default
""")
        print("✅ .env file created! Please update it with your database password.")
        return False
    return True

def main():
    """Main setup function"""
    print("🏨 Hotel Reservations Application Setup")
    print("="*50)
    
    # Check if .env file exists
    env_exists = create_env_file()
    if not env_exists:
        print("\n⚠️  Please update the .env file with your database password and run setup again.")
        return
    
    load_dotenv()
    
    # Install Python dependencies
    if not install_python_dependencies():
        return
    
    # Install PostgreSQL (macOS only)
    if sys.platform == "darwin":
        install_postgresql()
    else:
        print("⚠️  Please install PostgreSQL manually for your operating system")
        print("Visit: https://www.postgresql.org/download/")
    
    # Setup database
    if not setup_database():
        print("\n❌ Setup failed at database creation step")
        print("Please ensure PostgreSQL is running and credentials are correct in .env file")
        return
    
    # Seed database
    if not seed_database():
        print("\n❌ Setup failed at database seeding step")
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Ensure your AWS credentials are configured")
    print("2. Make sure Claude 3.7 Sonnet is enabled in Amazon Bedrock")
    print("3. Run: python hotel_agent.py")

if __name__ == "__main__":
    main()