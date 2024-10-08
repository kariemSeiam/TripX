from flask import jsonify

class ErrorHandler:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # Register error handlers
        @app.errorhandler(400)
        def bad_request(error):
            return jsonify({"message": "Bad request"}), 400

        @app.errorhandler(401)
        def unauthorized(error):
            return jsonify({"message": "Unauthorized"}), 401

        @app.errorhandler(404)
        def not_found(error):
            return jsonify({"message": "Not found"}), 404

        @app.errorhandler(403)
        def forbidden(error):
            return jsonify({"message": "Forbidden"}), 403

        @app.errorhandler(500)
        def internal_server_error(error):
            return jsonify({"message": "Internal server error"}), 500
