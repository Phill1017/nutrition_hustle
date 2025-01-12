from flask import jsonify
from api.repositories.recipe_repository import RecipeRepository

class RecipeController:
    def __init__(self):
        # Create connection to recipe repository
        self.repository = RecipeRepository()

    def top_10(self):
        recipes = self.repository.top_10()
        return jsonify(recipes)

    def read_all(self):
        # Get all recipes from the database
        recipes = self.repository.find_all()
        return jsonify(recipes), 200

    def create(self, recipe):
        try:
            # Validate recipe data
            if not all(key in recipe for key in ["recipe_title", "recipe_ingredients", "recipe_macros"]):
                return jsonify({"error": "Missing required recipe fields"}), 400

            # Create recipe and return its ID
            new_id = self.repository.create(recipe)
            return new_id, 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    def read_one(self, recipe_id):
        try:
            # Get recipe by ID
            recipe = self.repository.find_by_id(recipe_id)
            if not recipe:
                return jsonify({"error": "Recipe not found"}), 404
            return jsonify(recipe), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    def update(self, recipe_id, recipe):
        try:
            # Check if recipe exists
            if not self.repository.find_by_id(recipe_id):
                return jsonify({"error": "Recipe not found"}), 404
            
            # Update recipe
            updated_recipe = self.repository.update(recipe_id, recipe)
            return jsonify({"recipe_id": recipe_id}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    def delete(self, recipe_id):
        try:
            # Check if recipe exists
            if not self.repository.find_by_id(recipe_id):
                return jsonify({"error": "Recipe not found"}), 404
            
            # Delete recipe
            self.repository.delete(recipe_id)
            return "", 204
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

_controller = None

def get_controller():
    global _controller
    if _controller is None:
        _controller = RecipeController()
    return _controller

def read_all():
    return get_controller().read_all()

def create(recipe):
    return get_controller().create(recipe)

def read_one(recipe_id):
    return get_controller().read_one(recipe_id)

def update(recipe_id, recipe):
    return get_controller().update(recipe_id, recipe)

def delete(recipe_id):
    return get_controller().delete(recipe_id) 