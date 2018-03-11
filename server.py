from flask import Flask, request

node = Flask(__name__)

this_node_transaction = []

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

if __name__ == '__main__':
    node.run()