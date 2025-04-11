import requests
import random
from time import sleep

people = [
    'Cole',
    'Austin',
    'Zach',
    'Brandon',
    'Michael',
    'Jacob',
    'Matthew',
    'Joshua',
    'Nicholas',
    'Andrew',
    'Ryan',
    'David',
    'Daniel',
    'Christopher',
    'Anthony',
    'William',
    'Joseph',
    'Jonathan',
    'James',
    'Robert',
    'John',
    'Justin',
    'Kevin'
]

def generate_transactions(num_transactions=10):
    for _ in range(num_transactions):
        sender = random.choice(people)
        recipient = random.choice(people)
        amount = random.randint(1, 1000)
        
        response = requests.post('http://localhost:5000/transaction/new', json={
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        print(response.json())
        
        sleep(random.uniform(0.1, 2.0))  # Random delay between transactions
        
if __name__ == '__main__':
    while True:
        try:
            number = int(input("Enter number of transactions to generate (default 10): ") or 10)
            generate_transactions(number)
        except Exception as e:
            print(f"Error: {e}")
            sleep(5)
