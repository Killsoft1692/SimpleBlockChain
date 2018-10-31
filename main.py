#!/usr/bin/env python
import os
from flask_api import FlaskAPI
from flask_pymongo import PyMongo
from logging import FileHandler, WARNING
from settings import HOST, PORT

app = FlaskAPI(__name__)

app.config['MONGO_URI'] = os.environ.get('DB')

mongo = PyMongo(app)

log_handler = FileHandler('error_log.txt')
log_handler.setLevel(WARNING)
app.logger.addHandler(log_handler)

from views import *

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
