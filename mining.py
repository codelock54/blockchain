from flask import Flask, jsonify
from Blockchain import Blockchain

app = Flask(__name__)

blockchain = Blockchain()


# Minando un nuevo bloque
@app.route('/mine_block', methods=['GET'])
def mine_block():

    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block["proof"]
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': 'Felicidades, haz minado un bloque',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


# obteniendo cadena completa


@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {"chain": blockchain.chain, "length": len(blockchain.chain)}
    return jsonify(response), 200


# Validez de la cadena
@app.route('/is_valid', methods=['GET'])

def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {"message": "Todo bien. El Blockchain es valido"}

    else:
        response = {"message": "El Blockchain no es valido JAJA"}

    return jsonify(response), 200
# corriendo la app

app.run(host="0.0.0.0", port="5000")
