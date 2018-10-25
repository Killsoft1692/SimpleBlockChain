#!/usr/bin/env python
import os
from flask_api import FlaskAPI
from flask_pymongo import PyMongo
from settings import HOST, PORT

app = FlaskAPI(__name__)

app.config['MONGO_URI'] = os.environ.get('DB')

mongo = PyMongo(app)

from views import *

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
