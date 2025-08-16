from database import DatabaseManager

postgres = "postgres"
db_manager = DatabaseManager(
    db_name=postgres,
    host="localhost",
    password=postgres,
    port=5432,
    user=postgres,
)

# db_manager.reset_database()
db_manager.setup_database()
