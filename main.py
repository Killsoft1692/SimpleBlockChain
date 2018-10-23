#!/usr/bin/env python
from flask_api import FlaskAPI
from settings import HOST, PORT

app = FlaskAPI(__name__)

from views import *

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
