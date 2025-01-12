from flask import Flask, render_template, request, make_response, redirect, jsonify, url_for, session, flash
from functools import wraps
import requests

from config import CONFIG
from nutrition_api_shim import register_user, login_user, calculate_calories, add_recipe, list_of_recipes, get_recipe, update_recipe, delete_recipe

# Initialize Flask application
app = Flask(__name__)
# Set secret key for secure session management
app.secret_key = 'your_secret_key_here'

def login_required(f):
    @wraps(f)  # This preserves the original function's metadata
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Homepage route
@app.route("/", methods=["GET", "POST"])
@login_required
def homepage():
    calories = None
    if request.method == "POST":
        try:
            # Get user inputs
            age = int(request.form["age"])
            gender = request.form["gender"]
            height = float(request.form["height"])
            weight = float(request.form["weight"])
            activity_level = request.form["activity_level"]
            
            # Calculate calories using the API
            response = calculate_calories(age, gender, height, weight, activity_level)
            if isinstance(response, dict) and "calories_needed" in response:
                calories = response["calories_needed"]
            else:
                flash('Error calculating calories. Please try again.', 'error')
        except (ValueError, requests.exceptions.JSONDecodeError) as e:
            flash('Error calculating calories. Please try again.', 'error')
    
    # Display homepage
    return render_template("recipes/main.html", 
                         recipes=list_of_recipes(),
                         calories=calories)

# Route for adding new recipes
@app.route("/new/", methods=["GET", "POST"])
@login_required
def newrecipe():
    if request.method == "GET":
        return render_template("recipes/new_recipe.html")
    # Handle recipe submission
    elif request.method == "POST":
        recipe = {
            "recipe_title": request.form["recipe_title"],
            "recipe_ingredients": request.form["recipe_ingredients"],
            "recipe_macros": request.form["recipe_macros"]
        }
        # Add recipe and get its ID
        recipe["recipe_id"] = add_recipe(recipe["recipe_title"], 
                                       recipe["recipe_ingredients"], 
                                       recipe["recipe_macros"])
        return render_template("recipes/new_recipe.html", recipe_added=recipe)

    return make_response("Invalid request", 400)

# Route for deleting recipes
@app.route("/deleterecipe/<int:recipe_id>")
@login_required
def deleterecipe(recipe_id):
    delete_recipe(recipe_id)
    return redirect("/")

# Route for editing existing recipes
@app.route("/editrecipe/<int:recipe_id>", methods=["GET", "POST"])
@login_required
def editrecipe(recipe_id):
    # Display edit form with current recipe data
    if request.method == "GET":
        recipe = get_recipe(recipe_id)
        return render_template("recipes/edit_recipe.html", recipe=recipe)
    # Handle recipe update submission
    elif request.method == "POST":
        recipe = {
            "recipe_id": recipe_id,
            "recipe_title": request.form["recipe_title"],
            "recipe_ingredients": request.form["recipe_ingredients"],
            "recipe_macros": request.form["recipe_macros"],
        }
        update_recipe(recipe)
        return render_template("recipes/edit_recipe.html", recipe=recipe, recipe_updated=recipe)
    
    return make_response("Invalid request", 400)

#@app.route("/top_recipes", methods=["GET"])
#def top_recipes():
#    if request.method == "GET":
#        recipes = top_10()
#        return render_template("recipes/top_recipes.html", recipes=recipes)

# User registration route
@app.route("/register", methods=["GET", "POST"])
def register():
    # Display registration form
    if request.method == "GET":
        return render_template("auth/register.html")
    # Handle registration submission
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        
        # Validate password confirmation
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template("auth/register.html")
            
        # Attempt to register user
        response = register_user(username, password)
        
        # Handle registration errors
        if isinstance(response, tuple):
            status_code = response[1]
            error_message = response[0].get('error', 'Registration failed.')
            flash(error_message, 'error')
            return render_template("auth/register.html")
            
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return make_response("Invalid request", 400)

# User login route
@app.route("/login", methods=["GET", "POST"])
def login():
    # Display login form
    if request.method == "GET":
        return render_template("auth/login.html")
    # Handle login submission
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Attempt to login user
        if login_user(username, password):
            session['username'] = username
            return redirect(url_for('homepage'))
        else:
            flash('Invalid username or password', 'error')
            return render_template("auth/login.html")

    return make_response("Invalid request", 400)

# Calorie calculator route
@app.route("/calculate_calories", methods=["GET", "POST"])
@login_required
def calculate():
    # Display calculator form
    if request.method == "GET":
        return render_template("recipes/calculate_calories.html")
    # Handle calculation submission
    elif request.method == "POST":
        try:
            # Get user inputs
            age = int(request.form["age"])
            gender = request.form["gender"]
            height = float(request.form["height"])
            weight = float(request.form["weight"])
            activity_level = request.form["activity_level"]
            
            # Calculate calories
            response = calculate_calories(age, gender, height, weight, activity_level)
            
            # Display results
            if response and isinstance(response, dict) and "calories_needed" in response:
                calories = round(response["calories_needed"])
                return render_template("recipes/calculate_calories.html", calories=calories)
            else:
                flash('Error calculating calories. Please try again.', 'error')
                return render_template("recipes/calculate_calories.html")
                
        except (ValueError, requests.exceptions.RequestException) as e:
            flash('Error calculating calories. Please try again.', 'error')
            return render_template("recipes/calculate_calories.html")

    return make_response("Invalid request", 400)

# User logout route
@app.route("/logout")
def logout():
    # Remove username from session
    session.pop('username', None)
    return redirect(url_for('login'))



# Start the application if running directly
if __name__ == "__main__":
    app.run(
        host=CONFIG["frontend"]["listen_ip"],
        port=CONFIG["frontend"]["port"],
        debug=CONFIG["frontend"]["debug"]
    )
