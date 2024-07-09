from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from flasgger import Swagger

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assets.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    CORS(app)

    swagger_config = {
        "swagger": "2.0",
        "info": {
            "title": "API de Gestão de Ativos",
            "description": "API para gerenciamento de ativos financeiros",
            "version": "1.0.0",
            "contact": {
                "name": "Felipy Penha Botega"
            }
        },
        "host": "localhost:5000",
        "basePath": "/api", 
        "schemes": [
            "http",
            "https"
        ]
    }

    swagger = Swagger(app, template=swagger_config)
    
    from .models import Ativo
    with app.app_context():
        db.create_all()

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
