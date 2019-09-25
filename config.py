from os import environ

class Config:

    # General Config
    SECRET_KEY = environ.get('SECRET_KEY', 'dev')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

    # FS
    FS_PATH_STORE = environ.get("FS_PATH_STORE")
    

#print(Config.SQLALCHEMY_DATABASE_URI)