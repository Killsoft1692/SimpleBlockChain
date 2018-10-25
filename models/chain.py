from models.block import Block
from main import mongo


class Chain:
    __has_instances = False

    def __init__(self):
        if self.__has_instances:
            raise Exception('Chain already created')
        else:
            self.chain = [Block.create_genesis_block()] if mongo.db.blocks.count() == 0\
                else [Block(bl.get('prev_hash'), bl.get('data'), bl.get('timestamp'))
                      for bl in mongo.db.blocks.find({})]
            self.singleton()

    @classmethod
    def singleton(cls):
        cls.__has_instances = True

    def is_valid(self):
        reversed_chain = self.chain[::-1]
        for i, block in enumerate(reversed_chain, 1):
            if len(self.chain) > i:
                if block.previous_block_hash != reversed_chain[i].hash:
                    return False
        return True

    def get_chain(self):
        return self.chain
