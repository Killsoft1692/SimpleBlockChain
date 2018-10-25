from models.block import Block


class Chain:
    __has_instances = False

    def __init__(self):
        if self.__has_instances:
            raise Exception('Chain already created')
        else:
            self.chain = [Block.create_genesis_block()]
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
