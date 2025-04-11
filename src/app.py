from flask import Flask, render_template, request, jsonify, redirect, url_for
from blockchain import Blockchain, Block, Transaction
import time

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to the Blockchain API!"}), 200

# Add a new transaction
@app.route('/transaction/new', methods=['POST'])
def new_transaction():
    data = request.get_json()
    required_fields = ['sender', 'recipient', 'amount']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing fields"}), 400
    
    try:
        tx = Transaction(
            sender=data['sender'],
            recipient=data['recipient'],
            amount=data['amount'],
            timestamp=data['timestamp'] if 'timestamp' in data else None
        )
        blockchain.add_transaction(tx)
        return jsonify({"message": "Transaction added to the mempool"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Get pending transactions
@app.route('/transaction/pending', methods=['GET'])
def get_pending_transactions():
    transactions = blockchain.mempool
    return jsonify({"transactions": transactions}), 200

# Submit a new block
@app.route('/block/new', methods=['POST'])
def submit_block():
    data = request.get_json()
    
    try:
        block = Block(
            index=data['index'],
            transactions=data['transactions'],
            timestamp=data['timestamp'],
            previous_hash=data['previous_hash'],
            difficulty=data['bits'],
            nonce=data['nonce']
        )
        result = blockchain.add_block(block)
        return (jsonify({"message": "Block added to the chain"}), 201) if result else (jsonify({"error": "Invalid block"}), 400)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# View the last block
@app.route('/block/last', methods=['GET'])
def get_last_block():
    last_block = blockchain.get_last_block().to_dict()
    return jsonify({"block": last_block}), 200

# Visual representation of the transactions
@app.route('/mempool', methods=['GET'])
def mempool_page():
    return render_template('mempool.html')

@app.route('/mempool/live', methods=['GET'])
def mempool_live_data():
    return jsonify({
        'mempool': blockchain.mempool,
        'count': len(blockchain.mempool)
    })
    
# Visual representation of the blockchain
@app.route('/blockchain', methods=['GET'])
def blockchain_page():
    return render_template('blockchain.html')

@app.route('/blockchain/live', methods=['GET'])
def blockchain_live_data():
    return jsonify({
        'blockchain': [block.to_dict() for block in blockchain.chain],
        'count': len(blockchain.chain)
    })
    
@app.route('/transaction/create', methods=['GET'])
def transaction_form():
    return render_template('create_transaction.html')

@app.route('/transaction/create', methods=['POST'])
def submit_transaction():
    sender = request.form.get('sender')
    recipient = request.form.get('recipient')
    amount = request.form.get('amount')

    if not sender or not recipient or not amount:
        return "Missing fields", 400

    try:
        amount = round(float(amount), 8)
        tx = Transaction(sender, recipient, amount)
        blockchain.add_transaction(tx)
        return redirect(url_for('mempool_page'))
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    print('Creating the blockchain...')
    blockchain = Blockchain(difficulty=4)
    print('Genesis block created.')
    print('Starting the Flask server...')
    app.run(debug=False, port=5000)
