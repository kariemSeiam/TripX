import os
from app import create_app
from app.config import DevelopmentConfig  # Ensure the correct import

# Main entry point for the application
if __name__ == "__main__":
    # Use the fully qualified path for the configuration
    app = create_app(os.getenv('FLASK_CONFIG', 'app.config.DevelopmentConfig'))

    app.run()
