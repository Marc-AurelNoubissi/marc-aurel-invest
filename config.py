import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Clé secrète pour sécuriser les sessions
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'marc-aurel-invest-secret-key-2026'
    
    # Base de données
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///marc_aurel_invest.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email (pour les alertes plus tard)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))