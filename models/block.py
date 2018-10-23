import hashlib
import datetime


class Block:
    def __init__(self, previous_block_hash, data, timestamp):
        self.previous_block_hash = previous_block_hash
        self.data = data
        self.timestamp = timestamp
        self.hash = self.get_hash()

    @classmethod
    def create_genesis_block(cls):
        return cls(None, None, datetime.datetime.now())

    def get_hash(self):
        header = '{}{}{}'.format(str(self.previous_block_hash), str(self.data), str(self.timestamp)).encode()
        hash_in = hashlib.md5(header).hexdigest().encode()
        return hashlib.md5(hash_in).hexdigest()
