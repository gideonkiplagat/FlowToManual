import os
import sys
from pathlib import Path

# Add the backend directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Initialize extensions
db = SQLAlchemy()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Initialize extensions
    jwt = JWTManager(app)
    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*", async_mode='eventlet')

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.session_routes import session_bp
    from routes.export_routes import export_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(session_bp)
    app.register_blueprint(export_bp)

    # Create tables
    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)
    