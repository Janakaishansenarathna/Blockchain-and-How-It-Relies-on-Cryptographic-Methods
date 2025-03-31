import hashlib
import json
import time


class Block:
    """
    Represents a block in the blockchain.
    """

    def __init__(self, index, timestamp, transactions, previous_hash):
        """
        Initializes a new block.
        :param index: The index of the block in the blockchain.
        :param timestamp: The time the block was created.
        :param transactions: The list of transactions included in the block.
        :param previous_hash: The hash of the previous block in the chain.
        """
        self.index = index  # The index of the block
        self.timestamp = timestamp  # The timestamp of the block
        self.transactions = transactions  # The transactions in the block
        self.previous_hash = previous_hash  # The hash of the previous block
        self.nonce = 0  # Add nonce for Proof-of-Work
        self.hash = self.calculate_hash()  # Calculate the hash of the block

    def calculate_hash(self):
        """
        Calculates the hash of the block.
        :return: The hash of the block.
        """
        block_data = json.dumps(
            {
                "index": self.index,
                "timestamp": self.timestamp,
                "transactions": self.transactions,
                "previous_hash": self.previous_hash,
                "nonce": self.nonce,  # Include nonce in hash calculation
            },
            sort_keys=True,
        ).encode("utf-8")
        return hashlib.sha256(block_data).hexdigest()


# Initialize blockchain with a genesis block
blockchain = [
    Block(
        0,
        time.time(),
        ["Genesis Transaction: Blockchain Network Initialized on March 31, 2025 at 10:00 AM UTC"],
        "0000000000000000000000000000000000000000000000000000000000000000",
    )
]
# Difficulty of Proof-of-Work
difficulty = 4
target_time = 0.5  # Target time for mining a block in seconds


def mine_block(block, difficulty):
    """
    Implements Proof-of-Work by incrementing the nonce until a valid hash is found.
    A valid hash starts with a certain number of leading zeros, determined by the difficulty.
    :param block: The block to mine.
    :param difficulty: The difficulty level (number of leading zeros required).
    """
    start_time = time.time()
    while block.hash[:difficulty] != "0" * difficulty:
        block.nonce += 1
        block.hash = block.calculate_hash()
    end_time = time.time()
    mine_time = end_time - start_time
    print(f"Block mined! Hash: {block.hash}, Time: {mine_time:.2f}s")
    return mine_time


# Add three subsequent blocks with detailed transaction examples
for i in range(1, 4):
    try:
        start_time = time.time()
        new_block = Block(
            i,
            time.time(),
            [
                f"Transaction {i}: User {chr(65 + i - 1)} transfers {i*10} BTC to User {chr(65+i)} on March 31, 2025 at {10+i}:00 AM UTC"
            ],
            blockchain[-1].hash,
        )
        mine_time = mine_block(new_block, difficulty)  # Mine the block to meet the difficulty
        blockchain.append(new_block)  # Add the new block to the blockchain

        # Adjust difficulty
        if mine_time < target_time:
            difficulty += 1
            print(f"Increasing difficulty to {difficulty}")
        elif mine_time > target_time:
            difficulty -= 1
            difficulty = max(1, difficulty)  # Ensure difficulty is at least 1
            print(f"Decreasing difficulty to {difficulty}")
    except Exception as e:
        print(f"Error adding block {i}: {e}")

original_transaction = None  # Initialize original_transaction to None

# Display initial blockchain state
print("Initial Blockchain Structure (Before Tampering):")
for block in blockchain:
    print(f"Block {block.index}:")
    print(f" Timestamp: {block.timestamp}")
    print(f" Transactions: {block.transactions}")
    print(f" Previous Hash: {block.previous_hash}")
    print(f"Original Transaction in Block 2 (Before Tampering): {original_transaction}")

# Simulate tampering with Block 2
print("Simulating Tampering with Block 2:")  # Indicate that we are tampering with Block 2
try:
    original_transaction = blockchain[2].transactions[0]  # Store the original transaction
    blockchain[2].transactions[0] = "Tampered Transaction: User B fraudulently transfers 1,000 BTC to User C on March 31, 2025 at 12:00 PM UTC"  # Replace the original transaction with a tampered transaction
    blockchain[2].hash = blockchain[2].calculate_hash()  # Recalculate the hash of the block
except Exception as e:
    print(f"Error tampering with block 2: {e}")

# Display blockchain state after tampering
print("Blockchain Structure After Tampering Block 2:")
for block in blockchain:
    print(f"Block {block.index}:")
    print(f" Current Hash: {block.hash}")
    print(f" Previous Hash: {block.previous_hash}")
    if original_transaction is not None:
        print(f"Original Transaction in Block 2 (Before Tampering): {original_transaction}")
    else:
        print("Original Transaction in Block 2 (Before Tampering): Not available due to tampering error")
