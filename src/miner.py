import requests
import json
from time import sleep
import time

from blockchain import Blockchain, Block, Transaction


def miner(timestamp_offset=0):
    # Get the last block
    latest_block = requests.get('http://localhost:5000/block/last').json()['block']
    latest_block = Block(
        index=latest_block['index'],
        transactions=latest_block['transactions'],
        timestamp=latest_block['timestamp'],
        previous_hash=latest_block['previous_hash'],
        difficulty=latest_block['bits'],
        nonce=latest_block['nonce']
    )
    blockchain = Blockchain(difficulty=latest_block.bits, chain=[latest_block])
    
    while len(latest_transactions := requests.get('http://localhost:5000/transaction/pending').json()['transactions']) < 1:
        print("No transactions in mempool, waiting...")
        sleep(5) # Wait for at least 3 transactions in the mempool
        
    print(f"Found {len(latest_transactions)} transactions in mempool.  Mining...")
    
    transactions = [Transaction(
        sender=tx['sender'],
        recipient=tx['recipient'],
        amount=tx['amount'],
        timestamp=tx['timestamp']
    ) for tx in latest_transactions]
    
    new_block = Block(
        index=blockchain.get_last_block().index + 1,
        transactions=transactions,
        timestamp=time.time() + timestamp_offset,
        previous_hash=latest_block.hash,
        difficulty=blockchain.difficulty
    )
    new_block.mine()
    
    print(new_block.to_dict())
    
    # Submit the new block to the blockchain
    response = requests.post('http://localhost:5000/block/new', json=new_block.to_dict())
    if response.status_code == 201:
        print("Block added to the chain")
    else:
        print("Failed to add block:", response.json())

if __name__ == '__main__':
    time_offset = int(input("Enter time offset in seconds (default 0): "))
    
    while True:
        try:
            miner(time_offset)
        except Exception as e:
            print(f"Error: {e}")
            sleep(5)