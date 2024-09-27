import os
from app.extensions import db  # Ensure db is imported

class Config:
    """Base configuration with default settings."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT") or "your_salt_here"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///default.db')
    SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO', 'False').lower() in ['true', '1', 't']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_HEADERS = 'Content-Type'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'default_jwt_secret_key')
    BCRYPT_LOG_ROUNDS = 12
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True

    @staticmethod
    def init_db(app):
        """Initialize the database if it does not exist."""
        db_uri = os.environ.get('DATABASE_URL', 'sqlite:///default.db')
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri.replace('sqlite:///', '')
            if not os.path.exists(db_path):
                with app.app_context():
                    db.create_all()  # Create all tables if they do not exist

        # Handle pool settings for non-SQLite databases
        if not db_uri.startswith('sqlite:///'):
            # Set pool size and overflow for other databases
            SQLALCHEMY_POOL_SIZE = int(os.environ.get('SQLALCHEMY_POOL_SIZE', 5))
            SQLALCHEMY_MAX_OVERFLOW = int(os.environ.get('SQLALCHEMY_MAX_OVERFLOW', 10))
            app.config['SQLALCHEMY_POOL_SIZE'] = SQLALCHEMY_POOL_SIZE
            app.config['SQLALCHEMY_MAX_OVERFLOW'] = SQLALCHEMY_MAX_OVERFLOW

class DevelopmentConfig(Config):
    """Development configuration with debugging enabled."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL', 'sqlite:///dev_site.db')

class TestingConfig(Config):
    """Testing configuration with a separate database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL', 'sqlite:///test_site.db')

class ProductionConfig(Config):
    """Production configuration with secure settings."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///prod_site.db')
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    PREFERRED_URL_SCHEME = 'https'
