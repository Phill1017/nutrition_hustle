# This file acts as a bridge between the frontend and the API
# Handles all HTTP requests to the API endpoints

import requests
from config import CONFIG

print(f"API URL configured as: {CONFIG['api']['url']}")  # Debug print

# User authentication functions
def register_user(username, password):
    # Send registration request to API
    response = requests.post(f"{CONFIG['api']['url']}/register", 
                           json={"username": username, "password": password})
    if response.status_code != 201:
        return response.json(), response.status_code
    return response.json()

def login_user(username, password):
    # Send login request to API
    url = f"{CONFIG['api']['url']}/login"
    print(f"Attempting to connect to: {url}")  # Debug print
    response = requests.post(url, 
                           json={"username": username, "password": password})
    if response.status_code != 200:
        return False
    return True

# Calorie calculation function
def calculate_calories(age, gender, height, weight, activity_level):
    try:
        response = requests.post(f"{CONFIG['api']['url']}/calories", 
                               json={"age": age, "gender": gender, "height": height, 
                                    "weight": weight, "activity_level": activity_level})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

# Recipe management functions
def add_recipe(recipe_title, recipe_ingredients, recipe_macros):
    response = requests.post(f"{CONFIG['api']['url']}/recipes", 
                           json={"recipe_title": recipe_title, 
                                "recipe_ingredients": recipe_ingredients,
                                "recipe_macros": recipe_macros})
    return int(response.text)

def list_of_recipes():
    response = requests.get(f"{CONFIG['api']['url']}/recipes")
    return response.json()

def get_recipe(recipe_id):
    response = requests.get(f"{CONFIG['api']['url']}/recipe/{recipe_id}")
    return response.json()

def update_recipe(recipe):
    response = requests.put(f"{CONFIG['api']['url']}/recipe/{recipe['recipe_id']}", 
                          json=recipe)
    return int(response.json()["recipe_id"])

def delete_recipe(recipe_id):
    requests.delete(f"{CONFIG['api']['url']}/recipe/{recipe_id}")

def top_10():
    response = requests.get(f"{CONFIG['api']['url']}/top10")
    return response.json()



