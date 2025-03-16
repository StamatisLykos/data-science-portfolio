import time
import random
from hashlib import sha256
from kafka import KafkaProducer
from json import dumps
from pymongo import MongoClient
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# Kafka producer initialization
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda x: dumps(x).encode('utf-8'))

# Initialize MongoDB client
client = MongoClient('localhost', 27017)

# Access the database
db = client['ITC6107']

# Access the collection
blocks_collection = db['Blocks']

# Number of CPUs
num_cores = 4

def calculate_hash(block):
    sha = sha256()
    sha.update(str(block).encode())
    return sha.hexdigest()

def create_genesis_block():
    genesis_block = {
        "sequence_number": 0,
        "nonce": random.randint(0, 2 ** 32),
        "time_to_mine": 0,
        "transactions": ['Genesis block'],
        "previous_block_hash": '0'
    }
    return genesis_block

latest_sequence_number = 0

def mine_block(previous_hash, transactions):
    global latest_sequence_number

    start_time = time.time()

    sequence_number = latest_sequence_number + 1

    # Calculate nonce range for each worker
    nonce_range = (0, 2 ** 32)
    worker_id = sequence_number % num_cores
    num_blocks_per_worker = (2 ** 32) // num_cores
    nonce_range = (worker_id * num_blocks_per_worker, (worker_id + 1) * num_blocks_per_worker)

    nonce = nonce_range[0]

    block = {
        "sequence_number": sequence_number,
        "time_to_mine": 0,
        "transactions": transactions,
        "previous_block_hash": previous_hash,
        "nonce": 0
    }

    while True:
        block["nonce"] = nonce
        block_hash = calculate_hash(block)
        if block_hash[:3] == "000":
            latest_sequence_number = sequence_number
            block["time_to_mine"] = time.time() - start_time
            block["num_transactions"] = len(transactions)
            produce_block(block)
            return block
        nonce += 1

def produce_block(block):
    block_data = {
        "sequence_number": block["sequence_number"],
        "num_transactions": block["num_transactions"],
        "nonce": block["nonce"],
        "digest": calculate_hash(block),
        "time_to_mine": block["time_to_mine"]
    }
    producer.send('Blocks', value=block_data)

def store_block(block):
    blocks_collection.insert_one(block)

def main():
    sc = SparkContext("local[*]", "BlockchainMining")
    ssc = StreamingContext(sc, 120)

    def process_transactions(rdd):
        transactions = rdd.collect()
        latest_block = blocks_collection.find_one(sort=[('_id', -1)])

        if latest_block:
            previous_hash = calculate_hash(latest_block)  # Calculate hash of the latest block
            latest_sequence_number = latest_block.get("sequence_number", -1) + 1
        else:
            previous_hash = '0'  # Genesis block's hash
            latest_sequence_number = 0

        # Creating a list to store transactions
        transaction_list = []

        for transaction in transactions:
            if transaction:
                transaction_list.append(transaction)

        block = mine_block(previous_hash, transaction_list)
        store_block(block)
        print_blockchain()

    transactions_stream = ssc.socketTextStream('localhost', 9999)
    transactions_stream.window(120).foreachRDD(process_transactions)

    try:
        ssc.start()
        ssc.awaitTermination()
    except KeyboardInterrupt:
        print("Mining stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        producer.close()

def print_blockchain():
    blockchain = blocks_collection.find()
    print("Blockchain:")
    for block in blockchain:
        print(block)

if __name__ == "__main__":
    main()
