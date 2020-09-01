from os import environ

class Config:
    # General Config
    SECRET_KEY = environ.get('SECRET_KEY', 'dev')
    FLASK_APP = environ.get('FLASK_APP')
    #FLASK_ENV = environ.get('FLASK_ENV')
    #SQL_SERVER = environ.get('SQL_SERVER')
    SQL_SERVER = "S"

    # FS
    FS_PATH_STORE = environ.get("FS_PATH_STORE")
    print("FS_PATH_STORE=", FS_PATH_STORE)

    # Version
    VERSION_REQUEST_VALUES = environ.get("VERSION_REQUEST_VALUES", "HOSTNAME,OS")
    print("VERSION_REQUEST_VALUES", VERSION_REQUEST_VALUES)

    #
    AMBIENTE = environ.get("AMBIENTE", "DESE")
    print("AMBIENTE=", AMBIENTE)

    # Database
    DB_NAME = environ.get("DB_NAME", "bdseg")
    DB_USERNAME = environ.get("DB_USERNAME", "sist_rpsr")
    DB_PASSWORD = environ.get("DB_PASSWORD", "Ho1#h=j4")
    DB_PORT = environ.get("DB_PORT", "2002")
    DB_SERVER = environ.get("DB_SERVER", 'desesqlbdmg')

    # mssql+pymssql://sist_rpsr:Ho1#h=j4@desesqlbdmg:2002/bdseg
    # Database
    #SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_DATABASE_URI = "mssql+pymssql://"+DB_USERNAME+":"+DB_PASSWORD+"@"+DB_SERVER+":"+DB_PORT+"/"+DB_NAME
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

    print("DATABASE=", SQLALCHEMY_DATABASE_URI)

    # LOG
    LOG_ENABLED = environ.get("LOG_ENABLED", "false")
    LOG_USERNAME = environ.get("LOG_USERNAME")
    LOG_PASSWORD = environ.get("LOG_PASSWORD")
    LOG_HOST = environ.get("LOG_HOST")
    LOG_PORT = environ.get("LOG_PORT")
    LOG_EXCHANGE = environ.get("LOG_EXCHANGE")
    LOG_KEY = environ.get("LOG_KEY")

    print("LOG_ENABLED=", LOG_ENABLED)

#print(Config.SQLALCHEMY_DATABASE_URI + "END")
