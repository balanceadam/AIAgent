import os
from decimal import Decimal

from django.core.management.base import BaseCommand
from web3 import Web3

from assets import models, utils

# ----------------------------- Configuration -----------------------------

# Replace with your Ethereum node RPC URL (e.g., from Infura or Alchemy)
RPC_URL = "https://sepolia.infura.io/v3/cd308e5454a04fa09d2f7451cf2bf1de"

# Replace with your deployed FansProtocol contract address
CONTRACT_ADDRESS = "0xF6faD5a7E8AAb900D689886e5581cF66933ACEA5"

# Replace with the tokenId you want to query
TOKEN_ID = 1

# ----------------------------- ABI Definition -----------------------------

# Minimal ABI containing only the getBondingCurveInfo function
FANSPROTOCOL_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "tokenId", "type": "uint256"}],
        "name": "getBondingCurveInfo",
        "outputs": [
            {"name": "price", "type": "uint256"},
            {"name": "bondingCurveProgress", "type": "uint256"},
            {"name": "marketValue", "type": "uint256"},
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    }
]

# ----------------------------- Helper Functions -----------------------------


def connect_web3(rpc_url):
    """
    Connect to the Ethereum network via the provided RPC URL.
    """
    try:
        web3 = Web3(Web3.HTTPProvider(rpc_url))
        if not web3.is_connected():
            print("Failed to connect to the Ethereum network.")
            return None
        return web3
    except Exception as e:
        print(f"Error connecting to Web3: {e}")
        return None


def get_contract(web3, contract_address, abi):
    """
    Initialize the contract instance.
    """
    try:
        contract = web3.eth.contract(address=web3.to_checksum_address(contract_address), abi=abi)
        return contract
    except Exception as e:
        print(f"Error initializing contract: {e}")
        return None


def get_bonding_curve_info(contract, token_id):
    """
    Call the getBondingCurveInfo function of the contract.
    """
    try:
        price, progress, market_value = contract.functions.getBondingCurveInfo(token_id).call()
        return price, progress, market_value
    except Exception as e:
        print(f"Error calling getBondingCurveInfo: {e}")
        return None, None, None
# ----------------------------- Main Execution -----------------------------


def main():
    # Connect to Web3
    web3 = connect_web3(RPC_URL)

    # Initialize contract
    contract = get_contract(web3, CONTRACT_ADDRESS, FANSPROTOCOL_ABI)

    # Fetch bonding curve info
    price, progress, market_value = get_bonding_curve_info(contract, TOKEN_ID)

    # Format the values
    # price_formatted = format_wei(price)
    price_formatted = utils.format_wei(price)
    # progress_formatted = Decimal(progress) / Decimal(1e18)  # Assuming progress was multiplied by 1e18
    progress_formatted = utils.format_wei(progress)  # Assuming progress was multiplied by 1e18
    # market_value_formatted = format_wei(market_value)
    market_value_formatted = utils.format_wei(market_value)

    # Display the results
    print(f"Bonding Curve Information for Token ID {TOKEN_ID}:")
    print(f"---------------------------------------------")
    print(f"Current Price: {price_formatted} (in Wei)")
    print(f"Bonding Curve Progress: {progress_formatted}%")
    print(f"Market Value: {market_value_formatted} (in Wei)")


def update_price(web3, protocol: models.Protocol):
    contract = get_contract(web3, protocol.address, FANSPROTOCOL_ABI)
    if not contract:
        return
    price, progress, market_value = get_bonding_curve_info(contract, protocol.protocol_id)
    if not price:
        return
    # protocol.price = utils.format_wei(Decimal(price))
    protocol.market_value = utils.format_wei(Decimal(market_value))
    protocol.bonding_curve = utils.format_wei(Decimal(progress))
    protocol.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        # main()
        # return
        lock_file = '/tmp/e_project_get_price.lock'
        if os.path.exists(lock_file):
            print('process running')
            return
        with open(lock_file, 'w') as f:
            f.write("Running")
        try:
            web3 = connect_web3(RPC_URL)
            if not web3:
                print('web3 is not connected')
                return
            for p in models.Protocol.objects.filter(is_enabled=True):
                update_price(web3, p)
        finally:
            os.remove(lock_file)
