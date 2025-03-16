from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['ITC6107']

blocks_collection = db['Blocks']


def get_block_info(serial_number):
    block = blocks_collection.find_one({"sequence_number": serial_number})
    if block:
        nonce = block.get("nonce", "Nonce not found")
        digest = block.get("digest", "Digest not found")
        num_transactions = block.get("num_transactions", "Number of transactions not found")
        return {
            "nonce": nonce,
            "digest": digest,
            "num_transactions": num_transactions
        }
    else:
        return "Block not found"


def get_block_with_smallest_mining_time():
    block = blocks_collection.find_one({}, sort=[("time_to_mine", 1)])
    return block


def get_average_and_cumulative_mining_time():
    pipeline = [
        {"$group": {"_id": None, "avg_time": {"$avg": "$time_to_mine"}, "total_time": {"$sum": "$time_to_mine"}}}
    ]
    result = list(blocks_collection.aggregate(pipeline))
    if result:
        return result[0]
    else:
        return {"avg_time": 0, "total_time": 0}


def get_block_with_most_transactions():
    pipeline = [
        {"$sort": {"num_transactions": -1}},
        {"$limit": 1}
    ]
    block = list(blocks_collection.aggregate(pipeline))
    return block


if __name__ == "__main__":
    # Query 1:
    block_serial_number = 5
    print("Query 1:")
    print(get_block_info(block_serial_number))

    # Query 2
    print("\nQuery 2:")
    print(get_block_with_smallest_mining_time())

    # Query 3
    print("\nQuery 3:")
    print(get_average_and_cumulative_mining_time())

    # Query 4
    print("\nQuery 4:")
    print(get_block_with_most_transactions())
