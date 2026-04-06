import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-enterprise-key-2026'

    # FIX: We removed 'instance' from this line so it builds the DB safely in the main folder
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'cloud_dr.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'backups')
    ALLOWED_EXTENSIONS = {'pdf', 'zip', 'sql', 'db', 'bak', 'json', 'txt', 'gz'}

    ADMIN_DEFAULT_USERNAME = 'admin.sys'
    ADMIN_DEFAULT_PASSWORD = 'SuperSecretBank123!'