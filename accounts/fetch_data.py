from sqlalchemy import create_engine, text

# Define the database URL (update credentials if needed)
DATABASE_URL = "postgresql://postgres:@localhost:5432/test_db"  # Ensure your credentials are correct

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

def fetch_data():
    query = text("SELECT * FROM accounts_customuser;")  # Wrap the query with text() for SQLAlchemy compatibility
    with engine.connect() as connection:
        result = connection.execute(query)
        return [row for row in result]

# Test the function
try:
    data = fetch_data()
    print("Fetched Data:", data)
except Exception as e:
    print("Error:", e)
