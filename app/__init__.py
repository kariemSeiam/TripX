from flask import Flask
from flask_cors import CORS
from .extensions import db, migrate, jwt
from .middleware.error_handler import ErrorHandler
from .middleware.rate_limiter import RateLimiter
from .views.auth.auth_views import auth_bp
from .views.conversations.conversations_views import conversations_bp
from .views.notifications.notifications_views import notifications_bp
from .views.payments.payments_views import payments_bp
from .views.support.support_views import support_bp
from .views.vehicles.vehicles_views import vehicles_bp
from .views.trips.trips_views import trips_bp
from .views.requests.requests_views import requests_bp
from .views.promotions.promotions_views import promotions_bp
from .views.documents.documents_views import documents_bp
from .views.drivers.drivers_views import drivers_bp
from .views.withdrawals.withdrawals_views import withdrawals_bp
from .views.history.history_views import history_bp
from .views.ratings.ratings_views import ratings_bp
from .views.referrals.referrals_views import referrals_bp
from .views.user_views import user_bp
from app.config import Config

def create_app(config_name=None):
    app = Flask(__name__)

    # Initialize CORS
    CORS(app)  # Initialize CORS with the app

    # Load the configuration based on the config_name parameter
    config_class = config_name or Config
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register middleware
    ErrorHandler(app)
    RateLimiter(app)

    # Initialize the database
    Config.init_db(app)

    # Register blueprints
    register_blueprints(app)

    return app

def register_blueprints(app):
    """Register all blueprints for the application."""
    from .views.auth.auth_views import auth_bp
    from .views.conversations.conversations_views import conversations_bp
    from .views.notifications.notifications_views import notifications_bp
    from .views.payments.payments_views import payments_bp
    from .views.support.support_views import support_bp
    from .views.vehicles.vehicles_views import vehicles_bp
    from .views.trips.trips_views import trips_bp
    from .views.requests.requests_views import requests_bp
    from .views.promotions.promotions_views import promotions_bp
    from .views.documents.documents_views import documents_bp
    from .views.drivers.drivers_views import drivers_bp
    from .views.withdrawals.withdrawals_views import withdrawals_bp
    from .views.history.history_views import history_bp
    from .views.ratings.ratings_views import ratings_bp
    from .views.referrals.referrals_views import referrals_bp
    from .views.user_views import user_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(conversations_bp, url_prefix='/conversations')
    app.register_blueprint(notifications_bp, url_prefix='/notifications')
    app.register_blueprint(payments_bp, url_prefix='/payments')
    app.register_blueprint(support_bp, url_prefix='/support')
    app.register_blueprint(vehicles_bp, url_prefix='/vehicles')
    app.register_blueprint(trips_bp, url_prefix='/trips')
    app.register_blueprint(requests_bp, url_prefix='/requests')
    app.register_blueprint(promotions_bp, url_prefix='/promotions')
    app.register_blueprint(documents_bp, url_prefix='/documents')
    app.register_blueprint(drivers_bp, url_prefix='/drivers')
    app.register_blueprint(withdrawals_bp, url_prefix='/withdrawals')
    app.register_blueprint(history_bp, url_prefix='/history')
    app.register_blueprint(ratings_bp, url_prefix='/ratings')
    app.register_blueprint(referrals_bp, url_prefix='/referrals')
    app.register_blueprint(user_bp, url_prefix='/users')
