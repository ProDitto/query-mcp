import psycopg2
from psycopg2 import OperationalError, DatabaseError
import os

class DatabaseManager:
    """
    A class to manage interactions with a PostgreSQL database.
    Encapsulates connection handling, database resetting, and CRUD operations.
    """

    def __init__(self, db_name, user, password, host="localhost", port=5432):
        """
        Initializes the DatabaseManager.
        :param db_name: The name of the PostgreSQL database.
        :param user: The PostgreSQL username.
        :param password: The PostgreSQL password.
        :param host: The database host address (defaults to localhost).
        :param port: The connection port number (defaults to 5432).
        """

        with open("/workspaces/query-mcp/extra/log.txt", "w+") as f:
            f.write("DB Manager \n")

        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cursor = None
        # self._connect()
    
    def get_name(self):
        return f"{self.db_name} {self.host} {self.port}"

    def _connect(self):
        """
        Establishes a connection to the PostgreSQL database.
        """
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.conn.cursor()
            print(f"Connected to PostgreSQL database: {self.db_name}")
        except OperationalError as e:
            print(f"Error connecting to PostgreSQL database: {e}")

    def close_connection(self):
        """
        Closes the database connection.
        Commits any pending changes before closing.
        """
        if self.conn:
            self.conn.commit()
            self.conn.close()
            print("PostgreSQL database connection closed.")

    def reset_database(self):
        """
        Resets the database by dropping all tables in the public schema and recreating them.
        This effectively clears all data while preserving the database itself.
        """
        self.close_connection()  # Close the existing connection to allow dropping the schema
        
        # Connect to a default database (e.g., 'postgres') to drop the target database
        try:
            temp_conn = psycopg2.connect(user=self.user, password=self.password, host=self.host, port=self.port, dbname="postgres")
            temp_conn.autocommit = True  # Autocommit required for CREATE/DROP DATABASE operations
            temp_cursor = temp_conn.cursor()
            
            # Terminate active connections to the database to be dropped
            terminate_connections_sql = f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{self.db_name}';
            """
            temp_cursor.execute(terminate_connections_sql)

            drop_db_sql = f"DROP DATABASE IF EXISTS {self.db_name};"
            temp_cursor.execute(drop_db_sql)
            print(f"Database '{self.db_name}' dropped.")
            
            create_db_sql = f"CREATE DATABASE {self.db_name};"
            temp_cursor.execute(create_db_sql)
            print(f"Database '{self.db_name}' created.")

        except (OperationalError, DatabaseError) as e:
            print(f"Error during database reset: {e}")
        finally:
            if temp_conn:
                temp_cursor.close()
                temp_conn.close()

        self._connect()  # Reconnect to the newly created database

    def setup_database(self, schema_sql):
        """
        Sets up the database by executing a schema definition (e.g., CREATE TABLE statements).
        :param schema_sql: A string containing SQL statements to create tables.
        """
        try:
            if self.cursor:
                self.cursor.execute(schema_sql)
                self.conn.commit()
                print("PostgreSQL database schema created/updated successfully.")
        except DatabaseError as e:
            print(f"Error setting up PostgreSQL database schema: {e}")
            self.conn.rollback()

    # CRUD functions - Implement with proper error handling and parameterization
    def create_entry(self, table_name, data):
        """
        Inserts data into a PostgreSQL table.
        :param table_name: The name of the table.
        :param data: A dictionary containing column-value pairs.
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
        try:
            self.cursor.execute(sql, tuple(data.values()))
            self.conn.commit()
            print(f"Entry created in {table_name}.")
        except DatabaseError as e:
            print(f"Error creating entry in {table_name}: {e}")
            self.conn.rollback()

    def read_entries(self, table_name, condition=None):
        """
        Reads data from a PostgreSQL table.
        :param table_name: The name of the table.
        :param condition: Optional, a string for the WHERE clause (e.g., "id = %s").
        :return: Fetched data as a list of tuples or an empty list.
        """
        sql = f"SELECT * FROM {table_name}"
        if condition:
            sql += f" WHERE {condition}"
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except DatabaseError as e:
            print(f"Error reading entries from {table_name}: {e}")
            return []

    def update_entry(self, table_name, set_data, condition):
        """
        Updates data in a PostgreSQL table.
        :param table_name: The name of the table.
        :param set_data: A dictionary of column-value pairs for the SET clause.
        :param condition: A string for the WHERE clause (e.g., "id = %s").
        """
        set_clause = ', '.join([f"{key} = %s" for key in set_data.keys()])
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {condition};"
        try:
            self.cursor.execute(sql, tuple(set_data.values()))
            self.conn.commit()
            print(f"Entry updated in {table_name}.")
        except DatabaseError as e:
            print(f"Error updating entry in {table_name}: {e}")
            self.conn.rollback()

    def delete_entry(self, table_name, condition):
        """
        Deletes data from a PostgreSQL table.
        :param table_name: The name of the table.
        :param condition: A string for the WHERE clause (e.g., "id = %s").
        """
        sql = f"DELETE FROM {table_name} WHERE {condition};"
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            print(f"Entry deleted from {table_name}.")
        except DatabaseError as e:
            print(f"Error deleting entry from {table_name}: {e}")
            self.conn.rollback()

# Example Usage
if __name__ == "__main__":
    # Ensure PostgreSQL is running and you have a user with appropriate permissions
    # Replace with your actual PostgreSQL credentials and database name
    db_manager = DatabaseManager(
        db_name="my_app_db",
        user="your_username",
        password="your_password"
    )

    # Define your database schema here
    schema = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS products (
        product_id SERIAL PRIMARY KEY,
        product_name TEXT NOT NULL,
        price REAL NOT NULL
    );
    """
    db_manager.setup_database(schema)

    # --- Demonstrate Resetting (optional) ---
    # db_manager.reset_database()  # This will wipe your data!

    # --- Demonstrate CRUD operations ---
    # Create
    db_manager.create_entry("users", {"name": "Charlie", "email": "charlie@example.com"})
    db_manager.create_entry("products", {"product_name": "Keyboard", "price": 75.50})

    # Read
    users = db_manager.read_entries("users")
    print("Users:", users)
    products = db_manager.read_entries("products", condition="price > 50")
    print("Products (price > 50):", products)

    # Update
    db_manager.update_entry("users", {"name": "Charles"}, condition="name = 'Charlie'")

    # Delete
    db_manager.delete_entry("products", condition="product_name = 'Keyboard'")

    db_manager.close_connection()
