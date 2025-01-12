import sqlite3
import sys

from config import CONFIG

class ExampleDB:
    @staticmethod
    def initialize(database_connection: sqlite3.Connection):
        cursor = database_connection.cursor()
        try:
            print("Dropping existing tables (if present)...")
            cursor.execute("DROP TABLE IF EXISTS account")
            cursor.execute("DROP TABLE IF EXISTS recipe")
        except sqlite3.OperationalError as db_error:
            print(f"Unable to drop table. Error: {db_error}")

        print("Creating tables...")
        cursor.execute(ExampleDB.CREATE_TABLE_ACCOUNT)
        cursor.execute(ExampleDB.CREATE_TABLE_RECIPE)
        database_connection.commit()

        print("Populating database with sample data...")
        cursor.executemany(ExampleDB.INSERT_ACCOUNT, ExampleDB.sample_account)
        cursor.executemany(ExampleDB.INSERT_RECIPE, ExampleDB.sample_recipe)
        database_connection.commit()

    CREATE_TABLE_ACCOUNT = """
        CREATE TABLE IF NOT EXISTS account (
            account_id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL COLLATE NOCASE,
            password TEXT NOT NULL,
            account_role TEXT NOT NULL
        )
        """

    CREATE_TABLE_RECIPE = """
    CREATE TABLE IF NOT EXISTS recipe (
        recipe_id INTEGER PRIMARY KEY,
        recipe_title TEXT NOT NULL,
        recipe_ingredients TEXT NOT NULL,
        recipe_macros TEXT NOT NULL
    )
    """

    INSERT_ACCOUNT = "INSERT INTO account VALUES (?, ?, ?, ?)"
    INSERT_RECIPE = "INSERT INTO recipe VALUES (?, ?, ?, ?)"

    sample_account = [
        (1, "Filip", "pass123", "admin"),
        (2, "Peter", "password123", "user"),
        (3, "Georgi", "psswrd123", "user"),
    ]

    sample_recipe = [
        (1, "Chicken & Rice", "Chicken Breast, Rice", "Calories: 1205cal, Protein:75g, Fats:10g, Carbs:100g"),
        (2, "Beef & Rice", "Beef, Rice", "Calories: 1455cal, Protein:95g, Fats:40g, Carbs:100g"),
        (3, "Fish & Rice", "Fish fillet, Rice", "Calories: 1005cal, Protein:65g, Fats:50g, Carbs:100g"),
    ]


def main():
    """Execute main function."""
    db_conn = sqlite3.connect(CONFIG["database"]["name"])
    db_conn.row_factory = sqlite3.Row

    ExampleDB.initialize(db_conn)
    db_conn.close()

    print("Database creation finished!")

    return 0

# --- Program entry ---
if __name__ == "__main__":
    sys.exit(main())
