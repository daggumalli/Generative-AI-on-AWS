# 🏨 Hotel Reservations Streamlit Frontend

A beautiful, user-friendly web interface for the Hotel Reservations Agent built with Streamlit.

## Features

### 📊 Dashboard
- Real-time statistics and metrics
- Hotel distribution by city
- Recent booking activity
- System status monitoring

### 💬 Chat Assistant
- Natural language conversations with the AI agent
- Real-time responses from AgentCore
- Chat history management
- Persistent conversation state

### ⚡ Quick Actions
- **Quick Hotel Search**: Search by city, state, and rating
- **Availability Check**: Check room availability for specific dates
- **Reservation Lookup**: Find bookings by email or reservation ID
- Form-based interactions for common tasks

### 🏨 Our Hotels
- Browse all available hotels
- Detailed hotel information and amenities
- Direct links to search rooms or chat about specific hotels
- Visual hotel cards with ratings and pricing

### 🔧 Admin Panel (Separate Page)
- Database statistics and analytics
- Recent activity monitoring
- Hotel and room management
- Data export capabilities
- System maintenance tools

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Database
Make sure your PostgreSQL database is running and configured in `.env`:
```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=hotels
DB_USER=postgres
DB_PASSWORD=your_password
```

### 3. Run the Application
```bash
# Option 1: Using the run script
python run_streamlit.py

# Option 2: Direct Streamlit command
streamlit run streamlit_app.py
```

### 4. Access the Application
- **Main App**: http://localhost:8501
- **Admin Panel**: http://localhost:8501/admin

## Application Structure

```
streamlit_app.py          # Main application with 4 pages
├── 📊 Dashboard          # Statistics and overview
├── 💬 Chat Assistant     # AI agent conversations
├── ⚡ Quick Actions      # Form-based interactions
└── 🏨 Our Hotels         # Hotel browsing

pages/
└── admin.py              # Admin panel (separate page)

.streamlit/
└── config.toml           # Streamlit configuration
```

## Pages Overview

### Dashboard Page
- **System Metrics**: Total hotels, rooms, reservations, cities
- **Visual Charts**: Hotels by city distribution
- **Recent Activity**: Latest bookings and reservations
- **System Status**: Database and agent connection status

### Chat Assistant Page
- **Natural Language Interface**: Talk to the AI agent naturally
- **Chat History**: Persistent conversation history
- **Real-time Responses**: Powered by AgentCore and Claude 3.7
- **Error Handling**: Graceful error messages and recovery

### Quick Actions Page
- **Hotel Search Form**: Search by location and rating criteria
- **Availability Checker**: Check room availability for specific dates
- **Reservation Lookup**: Find bookings by email or ID
- **Instant Results**: Quick form-based interactions

### Our Hotels Page
- **Hotel Gallery**: Browse all available hotels
- **Detailed Information**: Ratings, amenities, contact details
- **Quick Actions**: Direct links to search or chat about hotels
- **Visual Cards**: Beautiful hotel presentation

### Admin Panel
- **Database Statistics**: Comprehensive system metrics
- **Activity Monitoring**: Recent reservations and trends
- **Hotel Management**: View and manage hotel data
- **System Tools**: Data export and maintenance utilities

## Features in Detail

### 🎨 User Interface
- **Responsive Design**: Works on desktop and mobile
- **Custom Styling**: Beautiful CSS styling and themes
- **Interactive Elements**: Buttons, forms, and dynamic content
- **Visual Feedback**: Loading spinners, success/error messages

### 🔄 Real-time Updates
- **Live Data**: Direct database connections
- **Instant Responses**: Real-time agent conversations
- **Dynamic Content**: Auto-updating statistics and information
- **Session Management**: Persistent state across interactions

### 🛡️ Error Handling
- **Graceful Degradation**: Handles database and agent errors
- **User Feedback**: Clear error messages and guidance
- **Recovery Options**: Suggestions for resolving issues
- **System Status**: Connection monitoring and alerts

### 📱 Mobile Friendly
- **Responsive Layout**: Adapts to different screen sizes
- **Touch Friendly**: Optimized for mobile interactions
- **Fast Loading**: Efficient data loading and caching
- **Offline Indicators**: Clear status when services are unavailable

## Customization

### Styling
Edit the CSS in `streamlit_app.py` to customize:
- Colors and themes
- Layout and spacing
- Component styling
- Responsive breakpoints

### Configuration
Modify `.streamlit/config.toml` for:
- Server settings
- Theme colors
- Browser behavior
- Development options

### Features
Add new pages or functionality by:
1. Creating new functions in `streamlit_app.py`
2. Adding navigation options
3. Implementing new database queries
4. Extending the agent capabilities

## Troubleshooting

### Common Issues

**Database Connection Error**
- Check PostgreSQL is running
- Verify credentials in `.env` file
- Test connection with `psql`

**Agent Initialization Error**
- Verify AWS credentials are configured
- Check Claude 3.7 Sonnet is enabled in Bedrock
- Ensure all Python dependencies are installed

**Streamlit Won't Start**
- Check port 8501 is available
- Verify Streamlit is installed: `pip install streamlit`
- Try running with `--server.port 8502` for different port

**Chat Not Working**
- Check agent initialization status in sidebar
- Verify database connection is active
- Look for error messages in chat history

### Performance Tips

- **Database Queries**: Optimize queries for large datasets
- **Caching**: Use `@st.cache_data` for expensive operations
- **Session State**: Minimize data stored in session state
- **Images**: Optimize images and use appropriate formats

## Development

### Adding New Features
1. **New Pages**: Add functions to `streamlit_app.py` or create new files in `pages/`
2. **Database Queries**: Add new queries to interact with hotel data
3. **Agent Tools**: Extend the agent with new capabilities
4. **UI Components**: Create reusable Streamlit components

### Testing
- Test all forms and interactions
- Verify database operations work correctly
- Check error handling and edge cases
- Test on different screen sizes

### Deployment
For production deployment:
1. Set up proper environment variables
2. Configure database for production
3. Set up SSL/HTTPS
4. Use proper authentication
5. Monitor performance and logs

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review Streamlit documentation
3. Check AgentCore documentation
4. Create an issue in the repository

---

Built with ❤️ using Streamlit, AgentCore, and Amazon Bedrock