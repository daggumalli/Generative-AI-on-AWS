# Hotel Reservations Agent

A sophisticated hotel reservation system built with Amazon Bedrock AgentCore, Strands framework, and PostgreSQL. This application demonstrates how to create an AI-powered hotel booking assistant that can search hotels, check availability, make reservations, and manage bookings.

## Features

🏨 **Hotel Search**: Search hotels by location, rating, and price range
🗓️ **Availability Check**: Real-time room availability for specific dates  
📝 **Reservations**: Complete booking process with guest details
🔍 **Booking Management**: Look up and manage existing reservations
❌ **Cancellations**: Cancel reservations with proper verification
💾 **PostgreSQL Database**: Persistent storage with 10 sample hotels and 50 rooms
🌐 **Web Interface**: Beautiful Streamlit frontend with dashboard, chat, and quick actions
📊 **Admin Panel**: Comprehensive management and analytics interface

## Architecture

- **AgentCore with Strands**: AI agent framework for natural language interactions
- **Amazon Bedrock**: Claude 3.7 Sonnet model for intelligent responses
- **PostgreSQL**: Relational database for hotel, room, and reservation data
- **Custom Tools**: Specialized functions for hotel operations
- **Streamlit Frontend**: Beautiful web interface for user interactions

## Prerequisites

- **Python 3.10+**
- **PostgreSQL 15+** 
- **AWS Account** with Bedrock access
- **AWS CLI** configured with credentials
- **Claude 3.7 Sonnet** enabled in Amazon Bedrock

## Quick Start

### 1. Clone and Setup

```bash
# Navigate to the hotel-reservations directory
cd hotel-reservations

# Run the setup script
python setup.py
```

### 2. Configure Environment

Update the `.env` file with your database password:

```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=hotels
DB_USER=postgres
DB_PASSWORD=your_postgres_password

# AWS Configuration  
AWS_REGION=us-east-1
AWS_PROFILE=default
```

### 3. Run the Application

**Option A: Streamlit Web Interface (Recommended)**
```bash
# Run the web application
python run_streamlit.py

# Or directly with streamlit
streamlit run streamlit_app.py
```
Access at: http://localhost:8501

**Option B: Command Line Interface**
```bash
python hotel_agent.py
```

## Manual Setup (Alternative)

If the automatic setup doesn't work, follow these steps:

### 1. Install PostgreSQL

**macOS (Homebrew):**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Database

```bash
python database/setup.py
python database/seed_data.py
```

## Database Schema

### Hotels Table
- Basic hotel information (name, address, rating, amenities)
- 10 sample hotels across different US cities

### Rooms Table  
- Room details (type, price, occupancy, amenities)
- 5 rooms per hotel (50 total rooms)
- Different room types: Standard King/Queen, Deluxe Suite, Executive, Family

### Reservations Table
- Guest information and booking details
- Date validation and conflict prevention
- Status tracking (confirmed/cancelled)

## Sample Data

The application includes 10 hotels with realistic data:

1. **Grand Plaza Hotel** (New York, NY) - Luxury Manhattan hotel
2. **Seaside Resort** (Miami, FL) - Beachfront resort  
3. **Mountain View Lodge** (Denver, CO) - Mountain retreat
4. **Business Center Inn** (Chicago, IL) - Business hotel
5. **Historic Downtown Hotel** (Boston, MA) - Historic charm
6. **Desert Oasis Resort** (Phoenix, AZ) - Desert luxury
7. **Lakefront Retreat** (Seattle, WA) - Lakeside hotel
8. **City Center Suites** (Atlanta, GA) - Extended stay
9. **Vineyard Inn** (Napa, CA) - Wine country boutique
10. **Airport Express Hotel** (Las Vegas, NV) - Convenient location

## Usage Examples

### Search Hotels
```
"Find hotels in New York with a rating above 4.0"
"Show me hotels in Miami under $200 per night"
```

### Check Availability
```  
"Are there rooms available at Grand Plaza Hotel from 2025-03-15 to 2025-03-18?"
"What rooms are available at hotel ID 2 for next weekend?"
```

### Make Reservations
```
"I want to book room 101 from March 15-18 for John Smith, email john@email.com, phone 555-1234"
```

### Manage Bookings
```
"Look up my reservation for john@email.com"
"Cancel reservation ID 123 for john@email.com"
```

## Tools Available

1. **search_hotels()** - Search hotels by location and criteria
2. **get_available_rooms()** - Check room availability for dates
3. **make_reservation()** - Create new reservations
4. **get_reservation_details()** - Look up existing bookings
5. **cancel_reservation()** - Cancel reservations with verification

## Error Handling

- Date validation (proper format, future dates)
- Availability conflicts prevention
- Guest email verification for cancellations
- Database connection error handling
- Input validation and sanitization

## Customization

### Adding More Hotels
Edit `database/seed_data.py` to add more hotels and rooms.

### Modifying Room Types
Update the `room_types` array in the seed data script.

### Changing Business Rules
Modify the tools in `tools/hotel_tools.py` for different policies.

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running: `brew services start postgresql@15`
- Check credentials in `.env` file
- Verify database exists: `psql -l`

### AWS/Bedrock Issues  
- Confirm AWS credentials: `aws sts get-caller-identity`
- Enable Claude 3.7 Sonnet in Bedrock console
- Check region configuration

### Import Errors
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check Python path and virtual environment

## Development

### Project Structure
```
hotel-reservations/
├── database/
│   ├── setup.py          # Database initialization
│   ├── seed_data.py      # Sample data insertion
│   └── models.py         # Database connection utilities
├── tools/
│   └── hotel_tools.py    # AgentCore tools for hotel operations
├── pages/
│   └── admin.py          # Streamlit admin panel
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── hotel_agent.py        # Main agent application (CLI)
├── streamlit_app.py      # Web interface application
├── run_streamlit.py      # Streamlit launcher script
├── setup.py             # Automated setup script
├── requirements.txt     # Python dependencies
├── .env.example        # Environment template
├── streamlit_README.md  # Frontend documentation
└── README.md           # This file
```

### Adding New Features
1. Create new tools in `tools/hotel_tools.py`
2. Add tools to the agent in `hotel_agent.py`
3. Update the system prompt to describe new capabilities
4. Test thoroughly with various inputs

## License

This project is part of the Amazon Bedrock AgentCore samples and follows the same licensing terms.

## Support

For issues related to:
- **AgentCore/Strands**: Check the official documentation
- **Amazon Bedrock**: AWS Support or documentation
- **This Application**: Create an issue in the repository

---

Built with ❤️ using Amazon Bedrock AgentCore and Strands framework.
## W
eb Interface Features

### 📊 Dashboard
- Real-time hotel and reservation statistics
- Visual charts showing hotel distribution
- Recent booking activity
- System status monitoring

### 💬 Chat Assistant
- Natural language conversations with the AI agent
- Persistent chat history
- Real-time responses from AgentCore
- Error handling and recovery

### ⚡ Quick Actions
- **Hotel Search Form**: Search by city, state, and rating
- **Availability Checker**: Check room availability for dates
- **Reservation Lookup**: Find bookings by email or ID
- Form-based interactions for common tasks

### 🏨 Hotel Gallery
- Browse all available hotels with detailed information
- Visual hotel cards with ratings and amenities
- Direct links to search rooms or chat about hotels
- Mobile-friendly responsive design

### 🔧 Admin Panel
- Comprehensive database statistics
- Hotel and room management interface
- Recent activity monitoring
- Data export and system tools

## Web Interface Usage

### Starting the Web App
```bash
# Recommended: Use the launcher script
python run_streamlit.py

# Alternative: Direct streamlit command
streamlit run streamlit_app.py --server.port 8501
```

### Accessing the Interface
- **Main Application**: http://localhost:8501
- **Admin Panel**: http://localhost:8501/admin

### Navigation
The web interface includes four main sections:
1. **📊 Dashboard** - Overview and statistics
2. **💬 Chat Assistant** - AI agent conversations  
3. **⚡ Quick Actions** - Form-based interactions
4. **🏨 Our Hotels** - Hotel browsing and information

### Mobile Support
The interface is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- Different screen orientations