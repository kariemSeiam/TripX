from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

class RateLimiter:
    def __init__(self, app=None):
        self.limiter = Limiter(
            get_remote_address,
            app=app,
            default_limits=[app.config['RATE_LIMIT']]
        )

    def init_app(self, app):
        self.limiter.init_app(app)
