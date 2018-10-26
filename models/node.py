import requests
from operator import itemgetter
from main import mongo


class Node:
    nodes = set() if mongo.db.nodes.count == 0 \
        else set([node.get('url') for node in mongo.db.nodes.find({})])

    @classmethod
    def add_node(cls, node):
        cls.nodes.add(node)
        mongo.db.nodes.insert({'url': node})

    @classmethod
    def get_node_with_canonical_chain(cls):
        # Returns tuple with node that has largest chain and length of chain if nodes exists else None
        if cls.nodes:
            return max([(node, len(requests.get('{}/chain'.format(node)).json()))
                        for node in cls.nodes], key=itemgetter(1))
        return None
