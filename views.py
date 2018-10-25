import datetime
import requests
from main import app
from settings import BACON_API_URL
from models.block import Block
from models.chain import Chain
from flask_api import status


CHAIN = Chain()


@app.route('/', methods=['GET'])
def index():
    """ Simple BlockChain example
        Routes:
             - chain/ - get chain;
                available methods = ["GET"];
                success response = {
                    "data": "str",
                    "hash": "str",
                    "prev_hash": "str"
                    };
                error response = {"error": "str"}.
             - chain/add_block - add new block;
                available methods = ["POST"];
                response = {"data": "str"}.
    """
    return {'data': 'BlockChain APP'}, status.HTTP_200_OK


@app.route('/chain', methods=['GET'])
def get_chain():
    if CHAIN.is_valid():
        response = [{'data': item.data, 'prev_hash': str(item.previous_block_hash), 'hash': str(item.hash)} for item in
                    CHAIN.get_chain()], status.HTTP_200_OK
    else:
        response = {'error': 'chain is not valid'}, status.HTTP_400_BAD_REQUEST
    return response


@app.route('/chain/add_block', methods=['POST'])
def add_block():
    CHAIN.get_chain().append(Block(CHAIN.get_chain()[-1].hash, requests.get(BACON_API_URL).json()[0],
                       datetime.datetime.now()))
    return {'data': CHAIN.get_chain()[-1].data}, status.HTTP_201_CREATED
