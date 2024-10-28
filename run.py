#!flask/bin/python
import os
import sys

import logging
import threading
from flask import Flask
from threading import Thread
from config import load_configurations, configure_logging
from whatsapp import webhook_blueprint, message_queue, queue_worker

app = Flask(__name__)

with app.app_context():
    load_configurations(app)
    configure_logging()

app.register_blueprint(webhook_blueprint)

worker_thread = Thread(target=queue_worker, args=(app,), daemon=True)
worker_thread.start()

if __name__ == "__main__":
    logging.info("Flask app started")
    app.run(host="0.0.0.0", port=8000)



@app.teardown_appcontext
def shutdown_worker(exception=None):
    message_queue.put(None)  # Enviar um sinal para o worker encerrar
    worker_thread.join()
