import requests

class BTCWrapper:
  def __init__(self):
     self.base_url = 'https://blockchain.info/'
  def get_transaction(self,txn_hash):
    """
    Retrieves information about a specific Bitcoin transaction using Blockchain.info API.

    Args:
      txn_hash: The Bitcoin transaction hash.
  
    Returns:
        Json data:A dictionary representing the transaction or None if an error occurs.
    """
    response = requests.get(self.base_url + f'rawtx/{txn_hash}')

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error retrieving transaction for {txn_hash}: {response.status_code}")
        return None
  def get_wallet(self, wallet_hash):
    """
        Retrieves information about a specific Bitcoin Wallet using Blockchain.info API.

        Args:
            wallet_hash: The Bitcoin Wallet hash.

        Returns:
            Json data: A dictionary representing the Wallet or None if an error occurs.
        """
    response = requests.get(self.base_url + f'rawaddr/{wallet_hash}')
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error retrieving wallet for {wallet_hash}: {response.status_code}")
        return None