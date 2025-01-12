from config import CONFIG
import sqlite3

# This function helps turn database data into a format Python
def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

class AccountRepository:
    # This function connects to our database
    def get_connection(self):
        db_conn = sqlite3.connect(CONFIG["database"]["name"])
        db_conn.row_factory = dict_factory
        return db_conn

    # Look for a user by their username
    def find_by_username(self, username):
        db_conn = self.get_connection()
        cursor = db_conn.cursor()
        try:
            # Look up the username, ignoring upper/lowercase
            cursor.execute(
                "SELECT * FROM account WHERE username = ? COLLATE NOCASE", 
                (username,)
            )
            result = cursor.fetchone()
            return result
        finally:
            db_conn.close()

    # Create a new user account in the database
    def create_user(self, username, hashed_password, role):
        db_conn = self.get_connection()
        cursor = db_conn.cursor()
        try:
            # Add the new user to our database
            cursor.execute(
                "INSERT INTO account (username, password, account_role) VALUES (?, ?, ?)",
                (username, hashed_password, role)
            )
            db_conn.commit()
            # Get the ID of the new user we just created
            new_id = cursor.lastrowid
            return {"message": "User registered successfully", "id": new_id}
        except sqlite3.IntegrityError:
            raise ValueError("Username already exists")
        finally:
            db_conn.close()

    # Check if login details are correct
    def verify_credentials(self, username, hashed_password):
        db_conn = self.get_connection()
        cursor = db_conn.cursor()
        try:
            # Look for a user with matching username and password
            cursor.execute(
                "SELECT * FROM account WHERE username = ? COLLATE NOCASE AND password = ?", 
                (username, hashed_password)
            )
            user = cursor.fetchone()
            if not user:
                return None
            return user
        finally:
            db_conn.close() 