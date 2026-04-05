"""
India Population Prediction - Flask Application Factory
"""

from flask import Flask


def create_app():
    """Application factory pattern."""
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    app.config.from_object("src.config.Config")

    # Register routes
    from src.routes import main_bp, api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
