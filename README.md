# Blockchain-Python-Test-Server
A simple implementation of the block chain featuring a server and miner

## How to Run
In a terminal run `app.py`.

This should start the Bitcoin Mock Server.

Next run the `miner.py` file in a seperate terminal to start a mining process.

##### Optional:
Run the `transaction_maker.py` file in a seperate terminal to make some test transactions.

## Viewing the Blockchain
Go to http://localhost:5000/blockchain to view the current blocks.

If you want to make your own block go to http://localhost:5000/transaction/create and you can make your own
transactions there that get automatically pulled into the mempool.

Browse through the `app.py` file to find other endpoints you can access.
