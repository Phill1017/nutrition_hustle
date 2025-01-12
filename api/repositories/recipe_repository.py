from .account_repository import AccountRepository

class RecipeRepository:
    def __init__(self):
        self.get_connection = AccountRepository().get_connection

    def find_all(self):
        db_conn = self.get_connection()
        cursor = db_conn.cursor()
        try:
            cursor.execute("SELECT * FROM recipe")
            recipes = cursor.fetchall()
            return recipes
        finally:
            db_conn.close()

    def top_10(self):
        pass

    def create(self, recipe):
        db_conn = self.get_connection()
        cursor = db_conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO recipe (recipe_title, recipe_ingredients, recipe_macros) VALUES (?, ?, ?)""",
                (recipe.get("recipe_title"), 
                 recipe.get("recipe_ingredients"), 
                 recipe.get("recipe_macros"))
            )
            db_conn.commit()
            new_id = cursor.lastrowid
            return new_id
        finally:
            db_conn.close()

    def find_by_id(self, recipe_id):
        db_conn = self.get_connection()
        cursor = db_conn.cursor()
        try:
            cursor.execute("SELECT * FROM recipe WHERE recipe_id = ?", (recipe_id,))
            recipe = cursor.fetchone()
            return recipe
        finally:
            db_conn.close()

    def update(self, recipe_id, recipe):
        db_conn = self.get_connection()
        cursor = db_conn.cursor()
        try:
            cursor.execute(
                """UPDATE recipe SET recipe_title = ?, recipe_ingredients = ?, recipe_macros = ? WHERE recipe_id = ?""",
                (recipe.get("recipe_title"), 
                 recipe.get("recipe_ingredients"), 
                 recipe.get("recipe_macros"), 
                 recipe_id)
            )
            db_conn.commit()
            return self.find_by_id(recipe_id)
        finally:
            db_conn.close()

    def delete(self, recipe_id):
        db_conn = self.get_connection()
        cursor = db_conn.cursor()
        try:
            cursor.execute("DELETE FROM recipe WHERE recipe_id = ?", (recipe_id,))
            db_conn.commit()
        finally:
            db_conn.close() 