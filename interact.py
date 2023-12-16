import random
import time
import requests
import concurrent.futures
from web3 import Web3

last_tx_hash = None

# Replace with your Alchemy endpoint and API key
alchemy_endpoint = "https://eth-sepolia.g.alchemy.com/v2/f5CCM-LCyz4LDgyXg_V6Ihw6MPaBGxvl"

# Connect to Alchemy
w3 = Web3(Web3.HTTPProvider(alchemy_endpoint))

# Replace with your contract address and ABI
contract_address = "0xcBdA1230141F56E6f7c3d7DA5CCf6A899edFbD2e"
owner_address = "0x8d3c36D37914691405F97C404B45d3FBB2126DAb"
contract_abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"winner","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"AuctionEnded","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"bidder","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"BidPlaced","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"clearer","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyClear","type":"event"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"bids","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"emergencyClear","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"endAuction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"highestBid","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"highestBidder","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"placeBid","outputs":[],"stateMutability":"payable","type":"function"}]
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Replace with your private key
owner_private_key = "c4133c6262e78b9cc61bce9972c9c256a640cb5d9e205fb3e91f1bd395000324"

private_keys = ["84b4091e15267b50f6645d44bb96b4bc3179377daa2a8808b224d9f579be1cf1", "0ed7b2db696a63d09cfc3f1372d18b7edb019ce61a90907b2ebaba7b9d209ee6", "e0023eb49080755858a869113960ff7077c814201a2bc44ea5579686e27841ea", "873027b1d6b90ba91c01056abd2a344d2120a12eefd300adae90bb64817e263c", "ced74225be9e26fed49fd7384a21677b4a6217d479c2987e46df3f9494677a6f"]  # Add more private keys as needed

# Global variable to store tx_hash values
tx_hashes = []

# Function to place a random bid
def place_random_bid(private_key):
    account = w3.eth.account.from_key(private_key)
    account_address = account.address

    # Random bid between 500 and 1000 wei
    bid_amount = random.randint(500, 1000)

    current_gas_price = w3.eth.gas_price

    transaction = contract.functions.placeBid().build_transaction({
        'from': account_address,
        'gas': 100000,
        'gasPrice': current_gas_price,
        'value': bid_amount,
        'nonce': w3.eth.get_transaction_count(account_address),
    })

    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction).hex()
    tx_hashes.append(tx_hash)
    
    print(f"Bid placed by {account_address}. Bid amount: {bid_amount} wei. Transaction hash: {tx_hash}. Gas price: {current_gas_price}")
    time.sleep(random.uniform(0.5, 2))  # Add a random delay to avoid nonce issues

# Example usage
for private_key in private_keys:
    place_random_bid(private_key)
    #time.sleep(1)  # Add a delay to avoid nonce issues (if they come from the same account)
    # colocar tempo como random (sleep aleatorio)

#time.sleep(5)
# Etherscan API usage
    
# print(f"tx_hash used: {last_tx_hash}")
# api_url = "https://api-sepolia.etherscan.io/api"
# api_key = "YU3XW5GSVTD9SHYTGWFQDMYQYTQG5IICA9"

# params = {
#     "module": "transaction",
#     "action": "getstatus",
#     "txhash": last_tx_hash,
#     "apikey": api_key,
# }

# # Make the API request
# response = requests.get(api_url, params=params)
# print(f'this is the url: {response}')

# # Check if the request was successful (status code 200)
# if response.status_code == 200:
#     data = response.json()
#     print(f'data: {data}')

# Function to end the auction
def end_auction():
    account = w3.eth.account.from_key(owner_private_key)
    account_address = account.address

    # Fetching current gas price
    current_gas_price = w3.eth.gas_price

    # End the auction (only the owner can do this)
    if account.address == contract.functions.owner().call():
        transaction = contract.functions.endAuction().build_transaction({
            'from': owner_address,
            'gas': 50000,
            'gasPrice': current_gas_price,
            'nonce': w3.eth.get_transaction_count(owner_address),
        })
        signed_transaction = w3.eth.account.sign_transaction(transaction, owner_private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        print(f"Auction ended by the owner. Transaction hash: {tx_hash.hex()}. Gas price: {current_gas_price}")
        # Check the final state
        final_highest_bidder = contract.functions.highestBidder().call()
        final_highest_bid = contract.functions.highestBid().call()
        print(f"Final Highest Bidder: {final_highest_bidder}")
        print(f"Final Highest Bid: {final_highest_bid}")

        return tx_hash
    else:
        print("You are not the owner. Cannot end the auction.")

def call_emergency_clear():

    current_gas_price = w3.eth.gas_price

    # Build the transaction
    transaction = contract.functions.emergencyClear().build_transaction({
        'from': owner_address,
        'gas': 2000000,  # Adjust the gas limit as needed
        'gas_price': current_gas_price,  # Adjust the gas price as needed
        'nonce': w3.eth.get_transaction_count(owner_address),
    })

    # Sign the transaction
    signed_transaction = w3.eth.account.sign_transaction(transaction, owner_private_key)

    # Send the transaction
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

#     print(f'Transaction sent. Transaction hash: {transaction_hash.hex()}')

    final_highest_bidder = contract.functions.highestBidder().call()
    final_highest_bid = contract.functions.highestBid().call()

    # tx_hash = call_emergency_clear()
    # print(f'Emergency called. Transaction reverted to the address {final_highest_bidder}. Bid amount: {final_highest_bid}')

def check_confirmations(tx_hash):
    try:
        receipt = w3.eth.getTransactionReceipt(tx_hash)
        if receipt is not None:
            confirmations = w3.eth.blockNumber - receipt['blockNumber'] + 1
            return confirmations
    except Exception as e:
        print(f"Error checking confirmations for {tx_hash}: {e}")
    return 0  # Transaction not confirmed yet

def check_confirmations_periodically():
    while True:
        for tx_hash in tx_hashes:
            confirmations = check_confirmations(tx_hash)
            print(f'Transaction {tx_hash} has {confirmations} confirmations.')

            # Your logic based on the number of confirmations
            if confirmations >= 12:
                print(f'Transaction {tx_hash} is confirmed.')
        
        time.sleep(2)

# Start the periodic parallel confirmation check
#tx_hash = check_confirmations_periodically()

#time.sleep(30)
tx_hash = end_auction()

