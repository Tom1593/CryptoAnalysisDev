import requests
from dotenv import load_dotenv
import os

# ETHERSCAN_API_URL = 'https://api.etherscan.io/'

class ETHWrapper:
    def __init__(self) -> None:
        self.base_url = 'https://api.etherscan.io/'
        load_dotenv()

        self.ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
    
    def get_transaction(self,txn_hash):
        """
        Retrieves information about a specific Etherium transaction using Ehterscan.io API.

        Args:
            txn_hash: The Etherium transaction hash.
  
        Returns:
            Json data:A dictionary representing the transaction or None if an error occurs.
        """
        response = requests.get(self.base_url + f'api?module=proxy&action=eth_getTransactionByHash&txhash={txn_hash}&apikey={self.ETHERSCAN_API_KEY}')
        if response.status_code == 200:
            json = response.json()
            if json['result'] is not None:
                return json['result']
        print(f"Failed to fetch transaction data for transaction hash {txn_hash}.")
        return None
    
    def get_wallet(self, wallet_hash, limit=50):
        """
        Retrieves information about a specific Etherium Wallet using Ehterscan.io API.
        there are included parameters in the request:
            sort - to order by newest txn
            offset - no txns will be skipped
            limit - temporary, so we dont withrow thousends of txns 
        Args:
            wallet_hash: The Etherium Wallet hash.

        Returns:
            Json data: A dictionary representing the Wallet or None if an error occurs.
        """
        response = requests.get(self.base_url + f'api?module=account&action=txlist&address={wallet_hash}&sort=desc&offest=0&limit={limit}&apikey={self.ETHERSCAN_API_KEY}')
        if response.status_code == 200:
            json = response.json()
            if json['result'] is not None:
                return json['result']
        print(f"Failed to fetch transaction data for transaction hash {wallet_hash}.")
        return None
    
    def get_block_by_number(self,block_number):
        """
        Retrieves information about a specific Etherium block using Ehterscan.io API.

        Args:
            block_number: The Etherium block number.
  
        Returns:
            Json data:A dictionary representing the block or None if an error occurs.
        """
        response = requests.get(self.base_url + f'api?module=proxy&action=eth_getBlockByNumber&tag={block_number}&boolean=false&apikey={self.ETHERSCAN_API_KEY}')
        if response.status_code == 200:
            return response.json()
        print(f"Failed to fetch block data for block number {block_number}.")
        return None