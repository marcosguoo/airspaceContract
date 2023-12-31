import random
import time
from web3 import Web3

# Replace with your Alchemy endpoint and API key
alchemy_endpoint = "https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY"

# Connect to Alchemy
w3 = Web3(Web3.HTTPProvider(alchemy_endpoint))

# Replace with your contract address and ABI
contract_address = ""
owner_address = ""
contract_abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"winner","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"AuctionEnded","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"bidder","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"BidPlaced","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"clearer","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyClear","type":"event"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"bids","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"emergencyClear","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"endAuction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"highestBid","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"highestBidder","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"placeBid","outputs":[],"stateMutability":"payable","type":"function"}]
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Replace with your private key
owner_private_key = ""

def call_emergency_clear():

    # Build the transaction
    transaction = contract.functions.emergencyClear().build_transaction({
        'from': owner_address,
        'gas': 2000000,  # Adjust the gas limit as needed
        'gasPrice': w3.to_wei('50', 'gwei'),  # Adjust the gas price as needed
        'nonce': w3.eth.get_transaction_count(owner_address),
    })

    # Sign the transaction
    signed_transaction = w3.eth.account.sign_transaction(transaction, owner_private_key)

    # Send the transaction
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

    print(f'Transaction sent. Transaction hash: {transaction_hash.hex()}')

tx_hash = call_emergency_clear()
print('Emergency!')
