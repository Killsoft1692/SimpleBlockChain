import hashlib
import datetime
from main import mongo


class Block:
    def __init__(self, previous_block_hash, data, timestamp, save=False):
        self.previous_block_hash = previous_block_hash
        self.data = data
        self.timestamp = timestamp
        self.hash = self.get_hash()
        if save:
            self.save_to_db()

    @classmethod
    def create_genesis_block(cls):
        return cls(None, None, datetime.datetime.now(), save=True)

    def save_to_db(self):
        mongo.db.blocks.insert(
            {"prev_hash": str(self.previous_block_hash), "hash": str(self.hash), "data": str(self.data),
             "timestamp": str(self.timestamp)})

    def get_hash(self):
        header = '{}{}{}'.format(str(self.previous_block_hash), str(self.data), str(self.timestamp)).encode()
        hash_in = hashlib.md5(header).hexdigest().encode()
        return hashlib.md5(hash_in).hexdigest()
