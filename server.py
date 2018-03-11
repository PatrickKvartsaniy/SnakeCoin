from flask import Flask, request
from app import Block, create_genesis_block, next_block
import datetime as date
import json

node = Flask(__name__)

this_node_transaction = []

miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"

blockchain = [create_genesis_block()]

peer_nodes = []

mining = True


@node.route('/txion', methods=['POST'])
def transaction():
    if request.method == 'POST':
        new_txion = request.get_json()
        this_node_transaction.append(new_txion)

        print("New transaction!")
        print(f"FROM: {new_txion['from']}")
        print(f"TO: {new_txion['to']}")
        print(f"AMOUNT: {new_txion['amount']}\n")
        return "Transaction submission successful\n"

def proof_of_work(last_proof):
    incrementor = last_proof + 1
    #keep incrementing while 
    while not(incrementor % 9 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    
    return incrementor

@node.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain[len(blockchain) - 1]
    last_proof = last_block.data['proof_of_work']

    proof = proof_of_work(last_proof)

    this_node_transaction.append(
        {"from":"network", "to": miner_address,"ammount": 1}
    )

    new_block_data = {
        "proof-of-work": proof,
        "transaction": list(this_node_transaction)
    
    }
    
    new_block_index = last_block.index + 1
    new_block_timestamp = this_timestamp = date.datetime.now()
    last_block_hash = last_block.hash
    
    this_node_transaction[:] = []
    
    mine_block = Block(
        new_block_index,
        new_block_timestamp,
        new_block_data,
        last_block_hash
    )

    blockchain.append(mine_block)

    return json.dumps({
      "index": new_block_index,
      "timestamp": str(new_block_timestamp),
      "data": new_block_data,
      "hash": last_block_hash
  }) + "\n"

@node.route('/block', methods=['GET'])
def get_blocks():
    chain_to_send = blockchain

    for block in chain_to_send:
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data = str(block.data)
        block_hash = block.hash
        block = {
            "index": block_index,
            "timestamp": block_timestamp,
            "data": block_data,
            "hash": block.hash
        }
    chain_to_send = json.dumps(chain_to_send)
    return chain_to_send

def find_new_chains():
    other_chains = []
    for node_url in peer_nodes:
        block = request.get(node_url+'/blocks').content
        block = json.dumps(block)
        other_chains.append(block)
    return other_chains

def consensus():
    other_chains = find_new_chains()
    longest_chain = blockchain

    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain
    
    blockchain = longest_chain

if __name__ == '__main__':
    node.run()