import os
import sys
from pathlib import Path

# Add the backend directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from flask import Config, Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
# db = SQLAlchemy()
from models import db
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    # app.config.from_object(Config)
    app.config.from_pyfile('config.cfg')
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Initialize extensions
    jwt = JWTManager(app)
    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*", async_mode='eventlet')

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.session_routes import session_bp
    # from routes.export_routes import export_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(session_bp)
    # app.register_blueprint(export_bp)


    # Create tables
    with app.app_context():
        print("App registered with DB?", db.engine.url)
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)
    

# other installed
# pip install eventlet
