# API application file that sets up the web server
# Connexion to handle API requests based on the OpenAPI specification

import connexion
from config import CONFIG

# Create a new Flask application using Connexion
app = connexion.FlaskApp(__name__)

# Load the API specification from the YAML file
app.add_api("nutrition-api.yml")

# Start the server if this file is run directly
if __name__ == "__main__":
    app.run(
        host=CONFIG["server"]["listen_ip"],
        port=CONFIG["server"]["port"],
        debug=CONFIG["server"]["debug"]
    )
 