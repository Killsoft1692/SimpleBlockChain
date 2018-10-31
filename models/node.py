import requests
from operator import itemgetter
from main import mongo
from settings import IDENTIFIER


class Node:
    nodes = set() if mongo.db.nodes.count == 0 \
        else set([node.get('url') for node in mongo.db.nodes.find({})])

    def __init__(self, node):
        self.node = node

    def save(self):
        Node.nodes.add(self.node)
        mongo.db.nodes.insert({'url': self.node})

    def is_valid(self):
        if requests.get(self.node).status_code == 200:
            if requests.get(self.node).json().get('identifier') == IDENTIFIER:
                return True
        return False

    @classmethod
    def get_node_with_canonical_chain(cls):
        # Returns tuple with node that has largest chain and length of chain if nodes exists else None
        if cls.nodes:
            return max([(node, len(requests.get('{}/chain'.format(node)).json()))
                        for node in cls.nodes], key=itemgetter(1))
        return None
