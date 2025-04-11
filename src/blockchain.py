import time
import json
    
from utils import sha256d, compute_merkle_root

class Transaction:
    def __init__(self, sender, recipient, amount, timestamp=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = timestamp or time.time()
        
    def to_dict(self):
        return self.__dict__
    
    def __repr__(self):
        return json.dumps(self.to_dict(), indent=2)

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, difficulty, nonce=0):
        self.index = index
        self.transactions = [tx.to_dict() if hasattr(tx, 'to_dict') else tx for tx in transactions]
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.bits = difficulty
        self.merkle_root = compute_merkle_root(self.transactions)
        self.hash = self.calculate_hash()
        
    def calculate_hash(self):
        data = {
            'index': self.index,
            'transactions': self.transactions,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'bits': self.bits,
            'nonce': self.nonce,
            'merkle_root': self.merkle_root
        }
        block_string = json.dumps(data, sort_keys=True).encode()
        hash = sha256d(block_string)
        return hash
            
    def mine(self):
        while True:
            self.hash = self.calculate_hash()
            if self.hash.startswith('0' * self.bits):
                break
            self.nonce += 1
            
        return self
    
    def to_dict(self):
        return self.__dict__
            

class Blockchain:
    def __init__(self, difficulty=5, chain=[]):
        self.chain = chain
        self.mempool = []
        self.difficulty = difficulty
        if self.chain == []:
            self.create_genesis_block()
        
    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0", self.difficulty).mine()
        self.chain.append(genesis_block)
        
    def get_last_block(self):
        return self.chain[-1]
    
    def add_transaction(self, tx: Transaction):
        self.mempool.append(tx.to_dict())
        
    def add_block(self, block):
        if self.is_valid_new_block(block, self.get_last_block()):
            self.chain.append(block)
            # Remove transactions from the mempool that are included in the block
            for tx in block.transactions:
                self.mempool.remove(tx)
                
            return True
        return False
    
    def is_valid_new_block(self, new_block, previous_block):
        if previous_block.index + 1 != new_block.index:
            print("Invalid index")
            return False
        
        if previous_block.hash != new_block.previous_hash:
            print("Invalid previous hash")
            return False
        
        if new_block.hash != new_block.calculate_hash() or not new_block.hash.startswith('0' * self.difficulty):
            print("Invalid hash")
            return False
        
        if new_block.merkle_root != compute_merkle_root(new_block.transactions):
            print("Invalid merkle root")
            return False
        
        return True
        
        
if __name__ == '__main__':
    blockchain = Blockchain(difficulty=2)
    print("Genesis Block Hash:", blockchain.chain[0].hash)
    print(blockchain.get_last_block().to_dict())
    
    blockchain.add_transaction(Transaction('Alice', 'Bob', 1.5))
    blockchain.add_transaction(Transaction('Bob', 'Charlie', 2.0))
    blockchain.add_transaction(Transaction('Charlie', 'Alice', 0.5))
    
    blockchain.add_block(Block(
        index=blockchain.get_last_block().index + 1,
        transactions=blockchain.mempool.copy(),
        timestamp=time.time(),
        previous_hash=blockchain.get_last_block().hash,
        difficulty=blockchain.difficulty,
    ).mine())
    print(blockchain.get_last_block().to_dict())