from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'

    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.transactions import transactions_bp
    from app.routes.budget import budget_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(budget_bp)

    # Pages d'erreur personnalisées
    @app.errorhandler(404)
    def page_non_trouvee(e):
        return '''
        <div style="text-align:center; padding:80px; font-family:sans-serif;">
            <h1 style="font-size:5rem; color:#7c3aed;">404</h1>
            <h2>Page introuvable</h2>
            <p>La page que vous cherchez n'existe pas.</p>
            <a href="/" style="color:#7c3aed;">Retour au tableau de bord</a>
        </div>''', 404

    @app.errorhandler(500)
    def erreur_serveur(e):
        return '''
        <div style="text-align:center; padding:80px; font-family:sans-serif;">
            <h1 style="font-size:5rem; color:#ef4444;">500</h1>
            <h2>Erreur serveur</h2>
            <p>Une erreur inattendue s'est produite.</p>
            <a href="/" style="color:#7c3aed;">Retour au tableau de bord</a>
        </div>''', 500

    return app