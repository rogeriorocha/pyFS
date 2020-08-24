from application import create_app
from flask_rabmq import RabbitMQ


#app, rabbitMQ = create_app()
app = create_app()

if __name__ == "__main__":
    #rabbitMQ.run_consumer()
    app.run(host='0.0.0.0', debug=True, use_reloader=True)