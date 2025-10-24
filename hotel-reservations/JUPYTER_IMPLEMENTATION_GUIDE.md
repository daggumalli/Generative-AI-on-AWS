# Jupyter Notebook Implementation Guide

This guide provides step-by-step instructions to build and test the HG2 Hotel Reservation Agentic GenAI application using Jupyter notebooks for interactive development.

## Why Jupyter Notebooks?

- **Interactive Development**: Test each component step-by-step
- **Visual Feedback**: See results immediately after each cell execution
- **Easy Debugging**: Isolate and fix issues in individual cells
- **Documentation**: Combine code, outputs, and explanations
- **Experimentation**: Try different approaches without affecting main code

## Prerequisites Setup

### 1. Install Jupyter and Dependencies

**Option A: Using Terminal (Recommended)**
```bash
# Create virtual environment
python3 -m venv hotel-reservation-env
source hotel-reservation-env/bin/activate

# Install Jupyter
pip install jupyter jupyterlab

# Install project dependencies
pip install -r requirements.txt
```

**Option B: Using Jupyter Notebook Cells**
```python
# In Jupyter notebook cells, use ! for shell commands
!python3 -m venv hotel-reservation-env
!source hotel-reservation-env/bin/activate && pip install jupyter jupyterlab
!pip install -r requirements.txt
```

### 2. Launch Jupyter Lab

```bash
# Start Jupyter Lab
jupyter lab

# Or use Jupyter Notebook
jupyter notebook
```

## Notebook-Based Implementation Steps

### Step 1: Create Main Implementation Notebook

Create `hotel-reservations-implementation.ipynb` with the following cells:

#### Cell 1: Install Dependencies (if needed)
```python
# Install required packages if not already installed
import subprocess
import sys

def install_package(package):
    try:
        __import__(package)
        print(f"✅ {package} already installed")
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully")

# Install key packages
packages = ['python-dotenv', 'pandas', 'sqlalchemy', 'psycopg2-binary', 'strands-agents']
for package in packages:
    install_package(package)
```

#### Cell 2: Environment Setup and Imports
```python
# Environment Setup and Imports
import os
import sys
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, text
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.append(os.getcwd())

print("✅ Environment setup complete")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
```

#### Cell 3: Database Connection Test
```python
# Database Connection Test
def test_database_connection():
    try:
        # Test connection parameters
        db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'hotels')
        }
        
        print("Database Configuration:")
        for key, value in db_config.items():
            if key == 'password':
                print(f"  {key}: {'*' * len(value) if value else 'Not set'}")
            else:
                print(f"  {key}: {value}")
        
        # Test connection
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        print(f"\n✅ Database connection successful!")
        print(f"PostgreSQL version: {version[0]}")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

# Test the connection
connection_success = test_database_connection()
```

#### Cell 4: Database Schema Creation
```python
# Database Schema Creation
def create_database_schema():
    if not connection_success:
        print("❌ Cannot create schema - database connection failed")
        return False
    
    try:
        # Database URL for SQLAlchemy
        db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        engine = create_engine(db_url)
        
        with engine.connect() as conn:
            # Create hotels table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS hotels (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    address VARCHAR(500) NOT NULL,
                    city VARCHAR(100) NOT NULL,
                    state VARCHAR(50) NOT NULL,
                    zip_code VARCHAR(20) NOT NULL,
                    phone VARCHAR(20) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    rating DECIMAL(2,1) CHECK (rating >= 1.0 AND rating <= 5.0),
                    amenities TEXT[],
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Create rooms table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS rooms (
                    id SERIAL PRIMARY KEY,
                    hotel_id INTEGER REFERENCES hotels(id) ON DELETE CASCADE,
                    room_number VARCHAR(10) NOT NULL,
                    room_type VARCHAR(50) NOT NULL,
                    price_per_night DECIMAL(10,2) NOT NULL,
                    max_occupancy INTEGER NOT NULL,
                    amenities TEXT[],
                    is_available BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(hotel_id, room_number)
                )
            """))
            
            # Create reservations table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS reservations (
                    id SERIAL PRIMARY KEY,
                    room_id INTEGER REFERENCES rooms(id) ON DELETE CASCADE,
                    guest_name VARCHAR(255) NOT NULL,
                    guest_email VARCHAR(255) NOT NULL,
                    guest_phone VARCHAR(20),
                    check_in_date DATE NOT NULL,
                    check_out_date DATE NOT NULL,
                    total_amount DECIMAL(10,2) NOT NULL,
                    status VARCHAR(20) DEFAULT 'confirmed',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CHECK (check_out_date > check_in_date)
                )
            """))
            
            conn.commit()
            print("✅ Database schema created successfully!")
            
            # Verify tables
            result = conn.execute(text("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            """))
            tables = [row[0] for row in result.fetchall()]
            print(f"Created tables: {tables}")
            
            return True
            
    except Exception as e:
        print(f"❌ Schema creation failed: {e}")
        return False

# Create the schema
schema_success = create_database_schema()
```

#### Cell 5: Sample Data Insertion
```python
# Sample Data Insertion
def insert_sample_data():
    if not schema_success:
        print("❌ Cannot insert data - schema creation failed")
        return False
    
    try:
        db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        engine = create_engine(db_url)
        
        with engine.connect() as conn:
            # Check if data already exists
            result = conn.execute(text("SELECT COUNT(*) FROM hotels"))
            hotel_count = result.fetchone()[0]
            
            if hotel_count > 0:
                print(f"✅ Sample data already exists ({hotel_count} hotels)")
                return True
            
            # Insert sample hotels
            hotels_data = [
                ("Grand Plaza Hotel", "123 Main St", "New York", "NY", "10001", "555-0101", "info@grandplaza.com", 4.5, ["WiFi", "Pool", "Gym", "Restaurant"], "Luxury hotel in downtown Manhattan"),
                ("Seaside Resort", "456 Ocean Ave", "Miami", "FL", "33101", "555-0102", "info@seasideresort.com", 4.2, ["WiFi", "Pool", "Beach Access", "Spa"], "Beautiful oceanfront resort"),
                ("Mountain View Lodge", "789 Alpine Rd", "Denver", "CO", "80201", "555-0103", "info@mountainview.com", 4.0, ["WiFi", "Fireplace", "Hiking Trails"], "Cozy mountain retreat"),
            ]
            
            for hotel in hotels_data:
                conn.execute(text("""
                    INSERT INTO hotels (name, address, city, state, zip_code, phone, email, rating, amenities, description)
                    VALUES (:name, :address, :city, :state, :zip_code, :phone, :email, :rating, :amenities, :description)
                """), {
                    'name': hotel[0], 'address': hotel[1], 'city': hotel[2], 'state': hotel[3],
                    'zip_code': hotel[4], 'phone': hotel[5], 'email': hotel[6], 'rating': hotel[7],
                    'amenities': hotel[8], 'description': hotel[9]
                })
            
            # Insert sample rooms
            rooms_data = [
                (1, "101", "Standard", 150.00, 2, ["WiFi", "TV", "AC"]),
                (1, "102", "Deluxe", 200.00, 2, ["WiFi", "TV", "AC", "Balcony"]),
                (1, "201", "Suite", 350.00, 4, ["WiFi", "TV", "AC", "Kitchen", "Living Room"]),
                (2, "101", "Ocean View", 250.00, 2, ["WiFi", "TV", "AC", "Ocean View"]),
                (2, "102", "Beach Suite", 400.00, 4, ["WiFi", "TV", "AC", "Beach Access", "Kitchen"]),
                (3, "101", "Mountain View", 120.00, 2, ["WiFi", "TV", "Fireplace"]),
            ]
            
            for room in rooms_data:
                conn.execute(text("""
                    INSERT INTO rooms (hotel_id, room_number, room_type, price_per_night, max_occupancy, amenities)
                    VALUES (:hotel_id, :room_number, :room_type, :price_per_night, :max_occupancy, :amenities)
                """), {
                    'hotel_id': room[0], 'room_number': room[1], 'room_type': room[2],
                    'price_per_night': room[3], 'max_occupancy': room[4], 'amenities': room[5]
                })
            
            conn.commit()
            print("✅ Sample data inserted successfully!")
            
            # Display summary
            hotels_result = conn.execute(text("SELECT COUNT(*) FROM hotels"))
            rooms_result = conn.execute(text("SELECT COUNT(*) FROM rooms"))
            
            print(f"Total hotels: {hotels_result.fetchone()[0]}")
            print(f"Total rooms: {rooms_result.fetchone()[0]}")
            
            return True
            
    except Exception as e:
        print(f"❌ Data insertion failed: {e}")
        return False

# Insert sample data
data_success = insert_sample_data()
```

#### Cell 6: Verify Database Setup
```python
# Verify Database Setup
def verify_database_setup():
    if not data_success:
        print("❌ Cannot verify - data insertion failed")
        return
    
    try:
        db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        engine = create_engine(db_url)
        
        # Display hotels
        hotels_df = pd.read_sql("SELECT id, name, city, state, rating FROM hotels", engine)
        print("🏨 Hotels in Database:")
        print(hotels_df.to_string(index=False))
        
        print("\n" + "="*50 + "\n")
        
        # Display rooms
        rooms_df = pd.read_sql("""
            SELECT r.id, h.name as hotel_name, r.room_number, r.room_type, r.price_per_night
            FROM rooms r
            JOIN hotels h ON r.hotel_id = h.id
            ORDER BY h.name, r.room_number
        """, engine)
        print("🛏️ Rooms in Database:")
        print(rooms_df.to_string(index=False))
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")

# Verify the setup
verify_database_setup()
```

#### Cell 7: Test Hotel Tools
```python
# Test Hotel Tools
from tools.hotel_tools import search_hotels, get_available_rooms

# Test hotel search
print("🔍 Testing Hotel Search:")
print("="*40)

# Search for hotels in New York
ny_hotels = search_hotels(location="New York", min_rating=4.0)
print("Hotels in New York with rating >= 4.0:")
print(ny_hotels)

print("\n" + "="*40 + "\n")

# Test room availability
print("🛏️ Testing Room Availability:")
print("="*40)

# Check availability at hotel ID 1
available_rooms = get_available_rooms(hotel_id=1, check_in="2024-03-15", check_out="2024-03-18")
print("Available rooms at Grand Plaza Hotel (Mar 15-18, 2024):")
print(available_rooms)
```

#### Cell 8: Initialize and Test Agent
```python
# Initialize and Test Agent
from strands import Agent
from strands.models import BedrockModel
from tools.hotel_tools import (
    search_hotels, get_available_rooms, make_reservation,
    get_reservation_details, cancel_reservation, web_search
)

# System prompt
SYSTEM_PROMPT = """You are a helpful hotel reservation assistant. 
Help customers search hotels, check availability, make reservations, and manage bookings.
Always be professional and friendly."""

# Initialize model
print("🤖 Initializing AI Model...")
model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    temperature=0.3,
    region_name=os.getenv('AWS_REGION', 'us-east-1')
)

# Create agent
print("🏨 Creating Hotel Agent...")
agent = Agent(
    model=model,
    tools=[search_hotels, get_available_rooms, make_reservation, 
           get_reservation_details, cancel_reservation, web_search],
    system_prompt=SYSTEM_PROMPT
)

print("✅ Hotel Reservation Agent initialized successfully!")
```

#### Cell 9: Interactive Agent Testing
```python
# Interactive Agent Testing
def test_agent_conversation():
    test_queries = [
        "Find hotels in New York with good ratings",
        "Check availability at Grand Plaza Hotel for March 15-18, 2024",
        "What are some popular attractions in Miami?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}: {query}")
        print('='*60)
        
        try:
            response = agent(query)
            print(f"Agent Response:\n{response}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "-"*60)

# Run test conversations
test_agent_conversation()
```

#### Cell 10: Manual Agent Chat
```python
# Manual Agent Chat (Interactive)
print("🏨 Hotel Reservation Agent - Interactive Mode")
print("="*50)
print("Type your questions below. Type 'quit' to exit.")
print("="*50)

def chat_with_agent():
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n🏨 Thank you for using Hotel Reservations Assistant!")
                break
            
            if not user_input:
                continue
            
            print("\nAgent: ", end="")
            response = agent(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\n🏨 Thank you for using Hotel Reservations Assistant!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")

# Uncomment the line below to start interactive chat
# chat_with_agent()
print("💡 Uncomment the last line in this cell to start interactive chat")
```

### Step 2: Create Testing Notebook

Create `hotel-reservations-testing.ipynb` for comprehensive testing:

#### Testing Notebook Structure:
- **Cell 1**: Import testing libraries and setup
- **Cell 2**: Unit tests for individual tools
- **Cell 3**: Integration tests for agent workflows
- **Cell 4**: Performance benchmarking
- **Cell 5**: Error handling tests
- **Cell 6**: Database integrity tests

### Step 3: Create Analysis Notebook

Create `hotel-reservations-analysis.ipynb` for data analysis:

#### Analysis Notebook Structure:
- **Cell 1**: Database analytics and reporting
- **Cell 2**: Agent conversation analysis
- **Cell 3**: Performance metrics visualization
- **Cell 4**: Usage patterns and insights

## Notebook Best Practices

### 1. Cell Organization
- One logical function per cell
- Clear cell titles using markdown headers
- Proper error handling in each cell

### 2. Output Management
- Clear outputs before committing
- Use print statements for progress tracking
- Display results in readable formats

### 3. Environment Management
```python
# Always start notebooks with this cell
import os
import sys
from dotenv import load_dotenv

# Ensure consistent environment
load_dotenv()
sys.path.append(os.getcwd())

print("Environment loaded successfully")
```

### 4. Testing Integration
```python
# Add testing capabilities to any notebook
def test_function(func, expected_result, *args, **kwargs):
    try:
        result = func(*args, **kwargs)
        success = result == expected_result
        print(f"✅ Test passed: {func.__name__}" if success else f"❌ Test failed: {func.__name__}")
        return success
    except Exception as e:
        print(f"❌ Test error: {func.__name__} - {e}")
        return False
```

## Advantages of Notebook Implementation

1. **Step-by-Step Validation**: Verify each component works before proceeding
2. **Visual Debugging**: See intermediate results and data
3. **Interactive Development**: Modify and test code in real-time
4. **Documentation**: Combine code, results, and explanations
5. **Experimentation**: Try different approaches easily
6. **Sharing**: Easy to share working examples with team

## Next Steps

After completing the notebook implementation:
1. Convert working notebooks to production Python scripts
2. Create automated testing suites
3. Set up CI/CD pipelines
4. Deploy to production environment

The notebook approach provides a perfect development and testing environment for the Hotel Reservation Agent!