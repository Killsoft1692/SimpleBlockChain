import datetime
import requests
from flask import request, redirect
from flask_api import status
from main import app
from settings import BACON_API_URL, IDENTIFIER
from models.block import Block
from models.chain import Chain
from models.node import Node
from pagination import Pagination


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
             - /nodes - get or add nodes
                available methods = ["GET", "POST"];
                request = {"url": "http://example.com:8080"};
                response = ["str"].
    """
    return {'data': 'BlockChain APP', 'identifier': IDENTIFIER}, status.HTTP_200_OK


@app.route('/nodes', methods=["GET", "POST"])
def nodes():
    if request.method == "POST" and request.data.get('url'):
        new_node = Node(request.data['url'])
        if new_node.is_valid(request):
            new_node.save()
            response = list(Node.nodes), status.HTTP_201_CREATED
        else:
            response = {'error': 'node is not valid'}, status.HTTP_400_BAD_REQUEST
    else:
        response = list(Node.nodes), status.HTTP_200_OK
    return response


@app.route('/chain', defaults={'page': 1}, methods=['GET'])
@app.route('/chain/page=<int:page>')
def get_chain(page):
    data = Pagination([{'data': item.data, 'prev_hash': str(item.previous_block_hash), 'hash': str(item.hash)}
                       for item in CHAIN.get_blocks_list()])
    if page > data.page_count or page == 0:
        return {}, status.HTTP_404_NOT_FOUND
    canonical_node = Node.get_node_with_canonical_chain()
    if canonical_node:
        if canonical_node[1] <= len(CHAIN):
            if CHAIN.is_valid():
                response = data.paginated().get(page), status.HTTP_200_OK
            else:
                response = {'error': 'chain is not valid'}, status.HTTP_400_BAD_REQUEST
        else:
            # update target node chain here
            response = redirect('{}/chain'.format(canonical_node[0]))
    else:
        response = {'error': 'add nodes first'}, status.HTTP_400_BAD_REQUEST
    return response


@app.route('/chain/add_block', methods=['POST'])
def add_block():
    CHAIN.get_blocks_list().append(Block(CHAIN.get_blocks_list()[-1].hash, requests.get(BACON_API_URL).json()[0],
                                         datetime.datetime.now(), save=True))
    return {'data': CHAIN.get_blocks_list()[-1].data}, status.HTTP_201_CREATED
