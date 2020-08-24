from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from application.schedule import tl
from config import Config
from flask_rabmq import RabbitMQ
import logging


db = SQLAlchemy()

def create_app():
    """Construct the core application."""
    print("*** create_app")
    logging.basicConfig(
        format='%(asctime)s %(process)d,%(threadName)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO)

    logger = logging.getLogger(__name__)

    app = Flask("fs", instance_relative_config=False)

    # RabbitMQ
    app.config.setdefault('RABMQ_RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/')
    app.config.setdefault('RABMQ_SEND_EXCHANGE_NAME', 'flask_rabmq')
    app.config.setdefault('RABMQ_SEND_EXCHANGE_TYPE', 'topic')
    app.config.setdefault('RABMQ_SEND_POOL_SIZE', 2)
    app.config.setdefault('RABMQ_SEND_POOL_ACQUIRE_TIMEOUT', 5)

    #ramq = RabbitMQ()
    #ramq.init_app(app=app)

    #ramq.send({'message_id': 222222, 'a': 7}, routing_key='flask_rabmq.test')

    #app.config.from_object('config.Config')
    
    # Remover
    #app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
    #app.config["SQLALCHEMY_DATABASE_URI"] = 'mssql+pymssql://sist_rpsr:Ho1#h=j4@desesqlbdmg:2002/bdseg'
    app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = Config.SECRET_KEY

    #db.app = app
    db.init_app(app)
    
    tl.start(block=False)
    with app.app_context():
        # Imports
        from . import routes

        # Create tables for our models
        #db.create_all()

        #return app, ramq
        return app