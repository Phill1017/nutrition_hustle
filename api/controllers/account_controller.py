from flask import jsonify
import hashlib
from api.repositories.account_repository import AccountRepository

class AccountController:
    def __init__(self):
        self.repository = AccountRepository()

    def register_user(self, body):
        try:
            # Get username and password from the body
            username = body.get("username")
            password = body.get("password")

            # Check if username and password were provided
            if not username or not password:
                return jsonify({"error": "Missing username or password"}), 400

            # Check if username is already taken
            existing_user = self.repository.find_by_username(username)
            if existing_user:
                return jsonify({"error": "Username already exists"}), 409

            try:
                # Hash password and create user
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                result = self.repository.create_user(username, hashed_password, "user")
                return jsonify(result), 201
            except ValueError as e:
                return jsonify({"error": str(e)}), 409
                
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def login_user(self, body):
        try:
            # Get username and password that user typed
            username = body.get("username")
            password = body.get("password")

            # Make sure both username and password were provided
            if not username or not password:
                return jsonify({"error": "Missing username or password"}), 400

            # First check if user exists
            existing_user = self.repository.find_by_username(username)
            if not existing_user:
                return jsonify({"error": "Invalid credentials"}), 401

            # Hash password and verify credentials
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            authenticated_user = self.repository.verify_credentials(username, hashed_password)
            if not authenticated_user:
                return jsonify({"error": "Invalid credentials"}), 401

            return jsonify({"message": "Login successful", "user": authenticated_user}), 200
            
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

# Create one controller to use everywhere
account_controller = AccountController()

def register_user(body):
    return account_controller.register_user(body)

def login_user(body):
    return account_controller.login_user(body) 