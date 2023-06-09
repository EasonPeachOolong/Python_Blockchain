import hashlib
import json

from time import time
from uuid import uuid4


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        
    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain
        proof: <int> The proof given by the Proof of Work algorithm
        previous_hash: (Optional) <str> Hash of previous Block
        return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    
   def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block
        sender: <str> Address of the Sender
        receiver: <str> Address of the Recipient
        amount: <int> Amount
        return: <int> The index of the Block that will hold this transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'receiver': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        block: <dict> Block
        return: <str>
        """

        """
        We must make sure that the Dictionary is ordered, or we'll have inconsistent hashes.
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


    def last_block(self):
        return self.chain[-1]


    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        last_proof: <int>
        return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof


    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        last_proof: <int> Previous Proof
        proof: <int> Current Proof
        return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"