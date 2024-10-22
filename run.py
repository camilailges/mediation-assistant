#!flask/bin/python
from flask_session import Session
import os
import sys

import logging
from flask import Flask

from config import load_configurations, configure_logging
from whatsapp import webhook_blueprint

app = Flask(__name__)

load_configurations(app)
configure_logging()
app.register_blueprint(webhook_blueprint)

# @app.get("/webhook")
# def hello_world():
#     return "<p>Hello, World!</p>"


if __name__ == "__main__":
    logging.info("Flask app started")
    app.run(host="0.0.0.0", port=8000)

# app = Flask(__name__)

# host = "0.0.0.0" if "--docker" in sys.argv else "localhost"
# port = int(os.environ.get("PORT", 3000))

# if os.environ.get("DEBUG", False) == "True":
#     app.config["DEBUG"] = True
#     app.config['SESSION_TYPE'] = 'filesystem'
#     sess = Session()
#     sess.init_app(app)
#     app.run(host=host, port=port, debug=True)
# else:
#     app.config['SESSION_TYPE'] = 'filesystem'
#     sess = Session()
#     sess.init_app(app)
#     app.run(host=host, port=port, extra_files="api_type.py")
