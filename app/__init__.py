from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)
    
    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI", "sqlite:///scheduler.db")
    else:
        app.config.update(test_config)
    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-key-for-development-only")
    
    db.init_app(app)
    
    from app.controllers import appointment_bp
    from app.controllers.main_controller import main_bp
    
    # Registra os blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(appointment_bp)
    
    # Adiciona helpers para os templates
    @app.template_filter('date_format')
    def date_format(value, format='%Y-%m-%d'):
        if value:
            return value.strftime(format)
        return ""
    
    @app.template_filter('time_format')
    def time_format(value, format='%H:%M'):
        if value:
            return value.strftime(format)
        return ""
    
    @app.context_processor
    def utility_processor():
        def now():
            return datetime.now()
        return dict(now=now)
    
    with app.app_context():
        db.create_all()
    
    # Adiciona uma rota de atalho para a função principal de index
    @app.route('/')
    def index():
        from app.controllers.main_controller import index as main_index
        return main_index()
        
    return app 