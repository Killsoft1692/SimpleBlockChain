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

    def get_chain(self):
        return self.chain
