"""
Database models and connection utilities
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/hotels"
        self.engine = create_engine(self.db_url)
    
    def get_connection(self):
        return self.engine.connect()
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        with self.get_connection() as conn:
            result = conn.execute(text(query), params or {})
            if result.returns_rows:
                return [dict(row._mapping) for row in result.fetchall()]
            else:
                # For INSERT, UPDATE, DELETE operations, commit the transaction
                conn.commit()
                return result.rowcount

# Global database instance
db = DatabaseConnection()