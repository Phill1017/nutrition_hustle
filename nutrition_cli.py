import sys
import getpass
from nutrition_api_shim import (
    add_recipe, delete_recipe, update_recipe, list_of_recipes, get_recipe,
    calculate_calories, register_user, login_user
)

def clear_screen():
    print("\033[H\033[J", end="")

def print_header():
    print("=" * 50)
    print("NUTRITION & HUSTLE")
    print("=" * 50)

def get_menu_choice(menu_options):
    for key, value in menu_options.items():
        print(f"{key}. {value}")
    return input("\nSelect an option: ")

def get_recipe_details():
    return {
        "title": input("Title: "),
        "ingredients": input("Ingredients (comma-separated): "),
        "macros": input("Macros: ")
    }

def get_calorie_inputs():
    try:
        age = int(input("Age: "))
        gender = input("Gender (male/female): ").lower()
        height = float(input("Height (cm): "))
        weight = float(input("Weight (kg): "))
        
        activity_levels = {
            '1': 'sedentary',
            '2': 'light',
            '3': 'moderate',
            '4': 'active',
            '5': 'very_active'
        }
        
        print("\nActivity Levels:")
        print("1. Sedentary (little/no exercise)")
        print("2. Light (1-3 times/week)")
        print("3. Moderate (3-5 times/week)")
        print("4. Active (6-7 times/week)")
        print("5. Very Active (daily intense)")
        
        choice = input("Select activity level (1-5): ")
        return age, gender, height, weight, activity_levels.get(choice, 'sedentary')
    except ValueError:
        print("Invalid input. Please enter numbers where required.")
        return None

def show_recipes():
    recipes = list_of_recipes()
    if not recipes:
        print("\nNo recipes found.")
        return
    
    for recipe in recipes:
        print(f"\nID: {recipe['recipe_id']}")
        print(f"Title: {recipe['recipe_title']}")
        print(f"Ingredients: {recipe['recipe_ingredients']}")
        print(f"Macros: {recipe['recipe_macros']}")
        print("-" * 30)

def handle_login():
    username = input("Username: ")
    password = getpass.getpass("Password: ") 
    
    if login_user(username, password):
        print("\nLogin successful!")
        return username
    
    print("\nLogin failed: Invalid credentials")
    return None

def handle_register():
    username = input("Username: ")
    while True:
        password = getpass.getpass("Password: ")
        if password == getpass.getpass("Confirm Password: "):
            break
        print("Passwords don't match. Try again.")
    
    if register_user(username, password):
        print("\nRegistration successful!")
        return True
    print("\nRegistration failed.")
    return False

def main():
    """Main program loop handling all user interactions."""
    main_menu = {
        "1": "Login",
        "2": "Register",
        "3": "Exit"
    }

    user_menu = {
        "1": "List Recipes",
        "2": "Add Recipe",
        "3": "Edit Recipe",
        "4": "Delete Recipe",
        "5": "Calculate Calories",
        "6": "Logout"
    }


    while True:
        clear_screen()
        print_header()
        choice = get_menu_choice(main_menu)
        
        if choice == "1":  # Login
            username = handle_login()
            if username:
                while True:
                    clear_screen()
                    print_header()
                    print(f"User: {username}")
                    choice = get_menu_choice(user_menu)
                    
                    if choice == "1":    # List Recipes
                        show_recipes()
                    elif choice == "2":   # Add Recipe
                        recipe = get_recipe_details()
                        recipe_id = add_recipe(recipe["title"], recipe["ingredients"], recipe["macros"])
                        print(f"\nRecipe added with ID: {recipe_id}")
                    elif choice == "3":   # Edit Recipe
                        show_recipes()
                        try:
                            recipe_id = int(input("\nEnter Recipe ID to edit: "))
                            recipe = get_recipe(recipe_id)
                            if recipe:
                                new_details = get_recipe_details()
                                updated_recipe = {
                                    "recipe_id": recipe_id,
                                    "recipe_title": new_details["title"] or recipe["recipe_title"],
                                    "recipe_ingredients": new_details["ingredients"] or recipe["recipe_ingredients"],
                                    "recipe_macros": new_details["macros"] or recipe["recipe_macros"]
                                }
                                update_recipe(updated_recipe)
                                print("\nRecipe updated!")
                        except ValueError:
                            print("\nInvalid Recipe ID!")
                    elif choice == "4":   # Delete Recipe
                        show_recipes()
                        try:
                            recipe_id = int(input("\nEnter Recipe ID to delete: "))
                            delete_recipe(recipe_id)
                            print(f"\nRecipe {recipe_id} deleted!")
                        except ValueError:
                            print("\nInvalid Recipe ID!")
                    elif choice == "5":   # Calculate Calories
                        inputs = get_calorie_inputs()
                        if inputs:
                            age, gender, height, weight, activity = inputs
                            result = calculate_calories(age, gender, height, weight, activity)
                            if result and "calories_needed" in result:
                                print(f"\nDaily calorie needs: {round(result['calories_needed'])} calories")
                    elif choice == "6":   # Logout
                        print("\nLogging out...")
                        break
                    
                    input("\nPress Enter to continue...")
                    
        elif choice == "2":  # Register
            handle_register()
        elif choice == "3":  # Exit
            print("\nGoodbye!")
            break
            
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    sys.exit(main())
