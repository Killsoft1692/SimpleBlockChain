from main import mongo


class Node:
    nodes = set() if mongo.db.nodes.count == 0 \
        else set([node.get('url') for node in mongo.db.nodes.find({})])

    @classmethod
    def add_node(cls, node):
        cls.nodes.add(node)
        mongo.db.nodes.insert({'url': node})
