from .DatabaseWrapper import DatabaseWrapper  # Assuming database_wrapper.py in same directory
import json

class WalletDB(DatabaseWrapper):
  """
  Wrapper class for interacting with the wallet database.
  """
  def __init__(self, db_path):
    super().__init__(db_path)
    self._table_name = 'Wallets'  # Assuming 'Wallets' table
    self._create_table()

  def _create_table(self):
    super()._create_table(self._table_name)
    
  def get_wallet(self, wallet_hash):
    """
    Retrieves the row data for a specific wallet.

    Args:
      wallet_hash: The hash of the wallet.

    Returns:
      The raw data for the wallet or None if not found.
    """
    wallet = super().get(self._table_name,{'wallet_hash':wallet_hash})
    return wallet if wallet else None
  def get_wallet_info(self, wallet_hash):
    """
    Retrieves the JSON data for a specific wallet.

     Args:
      wallet_hash: The hash of the wallet.

    Returns:
      The raw JSON data for the wallet or None if not found.
      """
    wallet = super().get(self._table_name, {'wallet_hash': wallet_hash})
    if wallet:
      try:
        json_data = json.loads(wallet[0][2])
        return json_data
      except json.JSONDecodeError:
        print("Invalid JSON Data")
        return None
    else:
      return None

  def insert_wallet(self, wallet_hash, json_data) -> int|bool:
    """
    Inserts a new wallet entry into the database.

    Args:
      wallet_hash: The hash of the transaction.
      json_data: The raw JSON data retrieved from the Blockchain.info API.

    Returns:
      wallet_id if the transaction info was inserted successfully, False otherwise.
    """
    # duplicate key check logic (optional)
    dup = self.get(self._table_name, {'wallet_hash': wallet_hash})
    if dup:
      return dup[0][0]  # Already exists
    
    wallet_data = {
      'wallet_hash':wallet_hash,
      'json_data': json.dumps(json_data)
    }
    
    wallet_id = super().insert(self._table_name, wallet_data)
    
    if not wallet_id:
      print(f"could not insert wallet: {wallet_hash}")
      return False
    # print(f"inserted wallet {wallet_hash}")
    return wallet_id
    
