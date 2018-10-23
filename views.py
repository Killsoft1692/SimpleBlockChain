import datetime
import requests
from main import app
from settings import BACON_API_URL
from models.block import Block
from models.chain import Chain
from flask_api import status


CHAIN = Chain().get_chain()


@app.route('/', methods=['GET'])
def index():
    return {'data': 'BlockChain APP'}, status.HTTP_200_OK


@app.route('/chain', methods=['GET'])
def get_chain():
    return [{'data': item.data, 'prev_hash': str(item.previous_block_hash), 'hash': str(item.hash)} for item in
            CHAIN], status.HTTP_200_OK


@app.route('/chain/add_block', methods=['POST'])
def add_block():
    CHAIN.append(Block(CHAIN[-1].hash, requests.get(BACON_API_URL).json()[0],
                       datetime.datetime.now()))
    return {'data': CHAIN[-1].data}, status.HTTP_201_CREATED
