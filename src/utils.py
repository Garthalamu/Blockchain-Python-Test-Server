import hashlib
import json

def sha256d(data) -> str:
    """Perform double SHA-256 hashing.

    Args:
        data (str|bytes): data to hash
        
    Returns:
        str: double SHA-256 hash of the data
    """
    
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha256(hashlib.sha256(data).digest()).hexdigest()

def compute_merkle_root(transactions):
    if not transactions:
        return sha256d('')
    
    def hash_pair(a, b):
        return sha256d(a + b)
    
    layer = [sha256d(json.dumps(tx, sort_keys=True)) for tx in transactions]
    
    while len(layer) > 1:
        if len(layer) % 2 == 1:
            layer.append(layer[-1])
        layer = [hash_pair(layer[i], layer[i + 1]) for i in range(0, len(layer), 2)]
        
    return layer[0]