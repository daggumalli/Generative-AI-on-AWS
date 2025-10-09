"""
Database setup and initialization for Hotel Reservations system
"""
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def create_database():
    """Create the hotels database if it doesn't exist"""
    try:
        # Try to connect to the hotels database directly
        test_conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD'),
            database='hotels'
        )
        test_conn.close()
        print("✅ Database 'hotels' already exists")
    except psycopg2.OperationalError:
        # Database doesn't exist, try to connect to default database to create it
        try:
            # Connect to default postgres database
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                port=os.getenv('DB_PORT', '5432'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD'),
                database='postgres'
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            
            # Create database
            cursor.execute('CREATE DATABASE hotels')
            print("✅ Database 'hotels' created successfully")
            
            cursor.close()
            conn.close()
        except psycopg2.OperationalError as e:
            print(f"❌ Could not create database: {e}")
            print("Database 'hotels' should already exist, continuing...")

def create_tables():
    """Create tables for hotels and rooms"""
    db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/hotels"
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
        print("✅ Tables created successfully")

if __name__ == "__main__":
    create_database()
    create_tables()