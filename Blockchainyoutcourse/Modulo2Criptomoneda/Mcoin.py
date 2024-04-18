import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests # tomer los nodos correctos
from uuid import uuid4
from urllib.parse import urlparse

# parte 1 Armando un blockchain
class BlockchainMG:
    def __init__(self):  
        self.chain = []
        self.transactions = []
        self.create_block(proof=1, previous_hash='0')  # bloque génesis
        self.nodes = set()
        
    def add_node(self,address):
        parse_url = urlparse(address)
        self.nodes.add(parse_url.netlock)
        
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        
        for node in network:
            response = requests.get(f 'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json(['length'])
                chain = response.json(['chain'])
                
                if lenght > max_length and self.is_chain_valid(chain):
                    max_lenght = lenght
                    longest_chain = chain
                    
            if longest_chain = chain:
                self.chain = longest_chain
                return true
            return false
            
            
            

    def create_block(self, proof, previous_hash):  
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),  
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions' : self.transactions}
        self.transactions = []
        self.chain.append(block)  
        return block
    
    
    
    def add_transaction(self, sender, reciever, amount):
        self.transacrion.append({'sender': sender,
                                 'reciever': reciever,
                                 'amount': amount})
        previous_block = self.get_previous_block()
        return previous_block['index']+1
        
    def get_previous_block(self):  
        return self.chain[-1]  

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()

            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def hash(self, block): 
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()  

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False

            previous_block = block
            block_index += 1
        return True


# Minando el blockchain
app = Flask(__name__)

# creando una direccion para el puerto 5000
node_address = str(uuid4()).replace('-','')


# creando el blockchain
blockchain = BlockchainMG()

# Minando un nuevo bloque
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender= node_address, reciever = 'Martin', amount=1)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, You have mined the block!!!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}

    return jsonify(response), 200  # código http

# obtener la cadena completa
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}  
    return jsonify(response), 200

# Chekear la validez de la cadena de bloques
@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'Todo bien. El blockchain es válido'}
    else:
        response = {'message': 'Houston, tenemos un problema. El blockchain no es válido'}
    return jsonify(response), 200

# Corriendo el App
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
        
    
    
    
# agregando nueva transacción al blockchain 
@app.route('/add_transaction', methods=['POST'])

def ass_transacrion():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all (key in json for key in transaction_keys):
        return 'algun elemento de la transacción esta faltando', 400
    
    index = blockchain_add_transaction(json['sender'],json['reciever'],json['amount'])
    response = {'message': f 'La transaccion sera añadida al Bloque {index}'}
    return jsonify(response), 201

# Paso 3 - Descentralizando el Blockchain


#Conectando nuevos nodos
@app.route('/connect_node', methods=['POST'])
def connect_node():
    json = requesy.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 401
    for node in nodes:
        blockchain.add_node(node)
        response = {'message':'Todos los nodos están ahora conectados. El Martincoin cointiene los siguientes nodos:',
                    'total_nodes': list(blockchain.nodes)}
        return jsonify(response), 201




# Reemplazando la cadena por la más larga

@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'Los nodos tenian diferentes cadenas asi que la cadena fue reemplazada por la mas larga'
                    'new_chain': blockchain_chain}
        else:
        response = {'message': 'Todo bien. la cadena es la más larga'
                    'actual_chain': lockchain_chain}
    return jsonify(response), 200






    
    

        