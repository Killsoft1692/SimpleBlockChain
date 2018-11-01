import requests
from requests.exceptions import MissingSchema, InvalidSchema
from urllib.parse import urlparse
from json.decoder import JSONDecodeError
from operator import itemgetter
from main import mongo
from settings import IDENTIFIER


class Node:
    nodes = set() if mongo.db.nodes.count == 0 \
        else set([node.get('url') for node in mongo.db.nodes.find({})])

    def __init__(self, node):
        self.url = node

    @staticmethod
    def clean_url(url):
        return urlparse(url).netloc

    def save(self):
        Node.nodes.add(self.url)
        mongo.db.nodes.insert({'url': self.url})

    def is_valid(self, request=None):
        if request:
            if self.clean_url(self.url) == self.clean_url(request.url_root):
                return False
        try:
            if requests.get(self.url).status_code == 200:
                if requests.get(self.url).json().get('identifier') == IDENTIFIER:
                    return True
        except (MissingSchema, InvalidSchema, JSONDecodeError):
            pass
        return False

    @classmethod
    def get_node_with_canonical_chain(cls):
        # Returns tuple with node that has largest chain and length of chain if nodes exists else None
        if cls.nodes:
            return max([(node, len(requests.get('{}/chain'.format(node)).json()))
                        for node in cls.nodes], key=itemgetter(1))
        return None
