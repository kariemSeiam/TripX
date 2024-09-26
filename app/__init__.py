from flask import Flask
from flask_jwt_extended import JWTManager
from app.config import Config
from app.extensions import db, migrate, jwt
from app.models import User
from app.middleware.rate_limiter import RateLimiter
from app.middleware.error_handler import ErrorHandler
from app.middleware.authentication import Authentication

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    RateLimiter(app)
    ErrorHandler(app)
    Authentication(app)

    from app.views.auth.auth_views import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Import and register blueprints
    from app.views.auth.auth_views import auth_bp
    from app.views.drivers.drivers_views import drivers_bp
    from app.views.documents.documents_views import documents_bp
    from app.views.vehicles.vehicles_views import vehicles_bp
    from app.views.requests.requests_views import requests_bp
    from app.views.trips.trips_views import trips_bp
    from app.views.earnings.earnings_views import earnings_bp
    from app.views.payments.payments_views import payments_bp
    from app.views.withdrawals.withdrawals_views import withdrawals_bp
    from app.views.notifications.notifications_views import notifications_bp
    from app.views.conversations.conversations_views import conversations_bp
    from app.views.support.support_views import support_bp
    from app.views.referrals.referrals_views import referrals_bp
    from app.views.promotions.promotions_views import promotions_bp
    from app.views.ratings.ratings_views import ratings_bp
    from app.views.history.history_views import history_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(drivers_bp, url_prefix='/drivers')
    app.register_blueprint(documents_bp, url_prefix='/documents')
    app.register_blueprint(vehicles_bp, url_prefix='/vehicles')
    app.register_blueprint(requests_bp, url_prefix='/requests')
    app.register_blueprint(trips_bp, url_prefix='/trips')
    app.register_blueprint(earnings_bp, url_prefix='/earnings')
    app.register_blueprint(payments_bp, url_prefix='/payments')
    app.register_blueprint(withdrawals_bp, url_prefix='/withdrawals')
    app.register_blueprint(notifications_bp, url_prefix='/notifications')
    app.register_blueprint(conversations_bp, url_prefix='/conversations')
    app.register_blueprint(support_bp, url_prefix='/support')
    app.register_blueprint(referrals_bp, url_prefix='/referrals')
    app.register_blueprint(promotions_bp, url_prefix='/promotions')
    app.register_blueprint(ratings_bp, url_prefix='/ratings')
    app.register_blueprint(history_bp, url_prefix='/history')

    return app
