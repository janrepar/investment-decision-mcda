from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, static_folder='build')  # Point to the Svelte build folder
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app)

    # Serve the Svelte index.html for the root route
    @app.route('/')
    def serve():
        return send_from_directory(app.static_folder, 'index.html')


    # Serve other static assets
    @app.route('/<path:path>')
    def static_files(path):
        return send_from_directory(app.static_folder, path)

    # Initialize database and routes
    with app.app_context():
        from . import routes, models
        db.create_all()  # Create the database if it doesn't exist

    return app
