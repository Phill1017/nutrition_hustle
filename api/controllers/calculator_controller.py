from flask import jsonify

class CalculatorController:
    def __init__(self):
        # Activity level multipliers for calorie calculations 
        self.activity_multipliers = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725,
            "very_active": 1.9
        }

    def calculate_calories(self, body):
        try:
            # Validate inputs
            if not all([body.get("age"), body.get("gender"), 
                       body.get("height"), body.get("weight"), 
                       body.get("activity_level")]):
                return jsonify({"error": "Missing required fields"}), 400

            if body["gender"].lower() not in ["male", "female"]:
                return jsonify({"error": "Invalid gender"}), 400

            if body["activity_level"].lower() not in self.activity_multipliers:
                return jsonify({"error": "Invalid activity level"}), 400

            # Calculate BMR using the Mifflin-St Jeor Equation
            age = float(body["age"])
            gender = body["gender"].lower()
            height = float(body["height"])
            weight = float(body["weight"])
            activity_level = body["activity_level"].lower()

            bmr = (10 * weight) + (6.25 * height) - (5 * age)
            bmr = bmr + 5 if gender == "male" else bmr - 161

            # Calculate total daily calories
            calories = round(bmr * self.activity_multipliers[activity_level], 2)
            
            return jsonify({"calories_needed": calories}), 200
            
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal server error"}), 500

calculator_controller = CalculatorController()

def calculate_calories(body):
    return calculator_controller.calculate_calories(body) 