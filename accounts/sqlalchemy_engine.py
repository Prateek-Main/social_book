# accounts/sqlalchemy_engine.py

from sqlalchemy import create_engine

# Replace with your PostgreSQL connection details
DATABASE_URL = "postgresql://postgres@localhost:5432/testdb"

# Create an engine
engine = create_engine(DATABASE_URL)
