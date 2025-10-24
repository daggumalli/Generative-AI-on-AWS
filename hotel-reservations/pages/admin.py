"""
Admin page for Hotel Reservations Streamlit app
"""
import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime, date

# Add the parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import db

st.set_page_config(
    page_title="🔧 Admin Panel - Hotel Reservations",
    page_icon="🔧",
    layout="wide"
)

def display_database_stats():
    """Display detailed database statistics"""
    st.subheader("📊 Database Statistics")
    
    try:
        # Hotels stats
        hotels_stats = db.execute_query("""
            SELECT 
                COUNT(*) as total_hotels,
                AVG(rating) as avg_rating,
                MIN(rating) as min_rating,
                MAX(rating) as max_rating
            FROM hotels
        """)[0]
        
        # Rooms stats
        rooms_stats = db.execute_query("""
            SELECT 
                COUNT(*) as total_rooms,
                COUNT(CASE WHEN is_available = true THEN 1 END) as available_rooms,
                AVG(price_per_night) as avg_price,
                MIN(price_per_night) as min_price,
                MAX(price_per_night) as max_price
            FROM rooms
        """)[0]
        
        # Reservations stats
        reservations_stats = db.execute_query("""
            SELECT 
                COUNT(*) as total_reservations,
                COUNT(CASE WHEN status = 'confirmed' THEN 1 END) as confirmed_reservations,
                COUNT(CASE WHEN status = 'cancelled' THEN 1 END) as cancelled_reservations,
                SUM(CASE WHEN status = 'confirmed' THEN total_amount ELSE 0 END) as total_revenue
            FROM reservations
        """)[0]
        
        # Display stats in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🏨 Total Hotels", hotels_stats['total_hotels'])
            st.metric("⭐ Average Rating", f"{hotels_stats['avg_rating']:.2f}")
            st.metric("📈 Rating Range", f"{hotels_stats['min_rating']:.1f} - {hotels_stats['max_rating']:.1f}")
        
        with col2:
            st.metric("🏠 Total Rooms", rooms_stats['total_rooms'])
            st.metric("✅ Available Rooms", rooms_stats['available_rooms'])
            st.metric("💰 Avg Price/Night", f"${rooms_stats['avg_price']:.2f}")
        
        with col3:
            st.metric("🎫 Total Reservations", reservations_stats['total_reservations'])
            st.metric("✅ Confirmed", reservations_stats['confirmed_reservations'])
            st.metric("💵 Total Revenue", f"${reservations_stats['total_revenue']:.2f}")
    
    except Exception as e:
        st.error(f"Error fetching database statistics: {str(e)}")

def display_recent_activity():
    """Display recent reservations and activity"""
    st.subheader("📈 Recent Activity")
    
    try:
        recent_reservations = db.execute_query("""
            SELECT 
                res.id,
                res.guest_name,
                res.guest_email,
                res.check_in_date,
                res.check_out_date,
                res.total_amount,
                res.status,
                res.created_at,
                h.name as hotel_name,
                h.city,
                r.room_number,
                r.room_type
            FROM reservations res
            JOIN rooms r ON res.room_id = r.id
            JOIN hotels h ON r.hotel_id = h.id
            ORDER BY res.created_at DESC
            LIMIT 20
        """)
        
        if recent_reservations:
            df = pd.DataFrame(recent_reservations)
            df['created_at'] = pd.to_datetime(df['created_at'])
            df['check_in_date'] = pd.to_datetime(df['check_in_date'])
            df['check_out_date'] = pd.to_datetime(df['check_out_date'])
            
            # Format for display
            display_df = df[['id', 'guest_name', 'hotel_name', 'city', 'room_number', 
                           'check_in_date', 'check_out_date', 'total_amount', 'status', 'created_at']]
            
            st.dataframe(
                display_df,
                column_config={
                    "id": "Reservation ID",
                    "guest_name": "Guest Name",
                    "hotel_name": "Hotel",
                    "city": "City",
                    "room_number": "Room",
                    "check_in_date": st.column_config.DateColumn("Check-in"),
                    "check_out_date": st.column_config.DateColumn("Check-out"),
                    "total_amount": st.column_config.NumberColumn("Amount", format="$%.2f"),
                    "status": "Status",
                    "created_at": st.column_config.DatetimeColumn("Booked At")
                },
                use_container_width=True
            )
        else:
            st.info("No reservations found.")
    
    except Exception as e:
        st.error(f"Error fetching recent activity: {str(e)}")

def display_hotel_management():
    """Display hotel management interface"""
    st.subheader("🏨 Hotel Management")
    
    try:
        # Get all hotels
        hotels = db.execute_query("""
            SELECT h.*, 
                   COUNT(r.id) as room_count,
                   COUNT(res.id) as reservation_count
            FROM hotels h
            LEFT JOIN rooms r ON h.id = r.hotel_id
            LEFT JOIN reservations res ON r.id = res.room_id AND res.status = 'confirmed'
            GROUP BY h.id
            ORDER BY h.name
        """)
        
        if hotels:
            for hotel in hotels:
                with st.expander(f"🏨 {hotel['name']} ({hotel['city']}, {hotel['state']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**📍 Address:** {hotel['address']}")
                        st.write(f"**⭐ Rating:** {hotel['rating']}/5.0")
                        st.write(f"**📞 Phone:** {hotel['phone']}")
                        st.write(f"**📧 Email:** {hotel['email']}")
                    
                    with col2:
                        st.write(f"**🏠 Rooms:** {hotel['room_count']}")
                        st.write(f"**🎫 Active Reservations:** {hotel['reservation_count']}")
                        st.write(f"**🎯 Amenities:** {', '.join(hotel['amenities']) if hotel['amenities'] else 'None'}")
                    
                    st.write(f"**📝 Description:** {hotel['description']}")
                    
                    # Room details for this hotel
                    rooms = db.execute_query("""
                        SELECT r.*, 
                               COUNT(res.id) as reservation_count
                        FROM rooms r
                        LEFT JOIN reservations res ON r.id = res.room_id AND res.status = 'confirmed'
                        WHERE r.hotel_id = :hotel_id
                        GROUP BY r.id
                        ORDER BY r.room_number
                    """, {'hotel_id': hotel['id']})
                    
                    if rooms:
                        st.write("**🏠 Rooms:**")
                        rooms_df = pd.DataFrame(rooms)
                        st.dataframe(
                            rooms_df[['room_number', 'room_type', 'price_per_night', 'max_occupancy', 'is_available', 'reservation_count']],
                            column_config={
                                "room_number": "Room #",
                                "room_type": "Type",
                                "price_per_night": st.column_config.NumberColumn("Price/Night", format="$%.2f"),
                                "max_occupancy": "Max Guests",
                                "is_available": "Available",
                                "reservation_count": "Reservations"
                            },
                            use_container_width=True
                        )
    
    except Exception as e:
        st.error(f"Error loading hotel management data: {str(e)}")

def display_system_tools():
    """Display system management tools"""
    st.subheader("🔧 System Tools")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Database Operations**")
        
        if st.button("🔄 Refresh Database Stats"):
            st.rerun()
        
        if st.button("🧹 Clean Old Reservations"):
            try:
                # Delete cancelled reservations older than 30 days
                result = db.execute_query("""
                    DELETE FROM reservations 
                    WHERE status = 'cancelled' 
                    AND created_at < CURRENT_DATE - INTERVAL '30 days'
                """)
                st.success(f"Cleaned up old reservations. Rows affected: {result}")
            except Exception as e:
                st.error(f"Error cleaning reservations: {str(e)}")
    
    with col2:
        st.write("**Data Export**")
        
        if st.button("📊 Export Reservations CSV"):
            try:
                reservations = db.execute_query("""
                    SELECT 
                        res.*,
                        h.name as hotel_name,
                        h.city,
                        h.state,
                        r.room_number,
                        r.room_type
                    FROM reservations res
                    JOIN rooms r ON res.room_id = r.id
                    JOIN hotels h ON r.hotel_id = h.id
                    ORDER BY res.created_at DESC
                """)
                
                if reservations:
                    df = pd.DataFrame(reservations)
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name=f"reservations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No reservations to export.")
            except Exception as e:
                st.error(f"Error exporting data: {str(e)}")

def main():
    """Main admin page function"""
    st.title("🔧 Hotel Reservations - Admin Panel")
    
    # Check database connection
    try:
        db.execute_query("SELECT 1")
        st.success("✅ Database connection active")
    except Exception as e:
        st.error(f"❌ Database connection failed: {str(e)}")
        return
    
    # Admin tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Statistics", "📈 Activity", "🏨 Hotels", "🔧 Tools"])
    
    with tab1:
        display_database_stats()
    
    with tab2:
        display_recent_activity()
    
    with tab3:
        display_hotel_management()
    
    with tab4:
        display_system_tools()

if __name__ == "__main__":
    main()