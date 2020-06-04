from flask import Flask, jsonify
from flask_cors import CORS
from .config import app_config
from .models import db, bcrypt

# import user_api blueprint
from .controllers.UserControllers import user_api as user_blueprint


def create_app(env_name):
    """
        Create app
    """
    app = Flask(__name__)
    app.config.from_object(app_config[env_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # Initializing bcrypt, db, and CORS
    bcrypt.init_app(app)
    db.init_app(app)
    CORS(app)

    # All controllers defined here
    app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')

    @app.route('/', methods=['GET'])
    def index():
        return jsonify({'status': 'success', 'message': 'Fineoz API Homecredit V1'})

    return app
