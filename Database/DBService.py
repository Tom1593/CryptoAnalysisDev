from .wrappers.TransactionDBWrapper import TransactionDB
from .wrappers.WalletDBWrapper import WalletDB
from .wrappers.TransactionWalletDBWrapper import TransactionWalletDB
from Api.wrappers.BTCWrapper import BTCWrapper
from dotenv import load_dotenv
import os

class DBService:
  """
    Service class for managing database interactions (transactions & wallets)
    and database creation in a specified folder.

    Leverages environment variables for database folder path configuration.
    """
    
  def __init__(self):
    # Load environment variables from .env file
    load_dotenv()

    # Get database folder path from environment variable
    self.db_folder = os.getenv("DB_FOLDER")

    # Ensure folder exists (create if necessary)
    if not os.path.exists(self.db_folder):
        os.makedirs(self.db_folder)

    # Pre-construct database filenames (modify as needed)
    self.db_filenames = {
        "transactions": os.path.join(self.db_folder, os.getenv("BTC_TXN_DB")),
        "wallets": os.path.join(self.db_folder, os.getenv("BTC_WALLET_DB")),
        "txn_wallets": os.path.join(self.db_folder, os.getenv("BTC_TXN_WALLET_RELATION_DB")),
    }
    
    self.transactions = TransactionDB(self.db_filenames['transactions'])
    self.wallets = WalletDB(self.db_filenames['wallets'])
    self.txn_wallets = TransactionWalletDB(self.db_filenames['txn_wallets'])  # Instance of TransactionWalletDB
    self.btc_api = BTCWrapper()
    
  def extract_wallets_from_txn_json(self, txn_json):
    """
    Returns the required data from a transaction dict/json

    Args:
        txn_obj: txn data object from the Blockchain.info api
    
    Returns:
        A list of wallet hashes
    """
    wallet_hashes = []
    for sender_entry in txn_json['inputs']:
      inner_entry = sender_entry['prev_out']
      wallet_hashes.append(inner_entry['addr'])
    for receiver_entry in txn_json['out']:
      wallet_hashes.append(receiver_entry['addr'])
    return wallet_hashes
  def extract_txns_from_wallet_json(self, wallet_json,limit = 5):
    """
    Returns the required data from a wallet dict/json

    Args:
        wallet_json: txn data object from the Blockchain.info api
    
    Returns:
        A list of wallet hashes
    """
    txn_hashes = []
    for tx in wallet_json['txs']:
      txn_hashes.append(tx['hash'])
      if txn_hashes.__len__ == limit:
        break
    return txn_hashes
  
  def insert_transaction(self, txn_hash,ts ,json_data, wallet_hashes):
    """
    Inserts a transaction and its associations with wallets.

    Args:
      txn_hash: The hash of the transaction.
      json_data: The raw JSON data retrieved from the Blockchain.info API.
      wallet_hashes: A list of wallet hash strings involved in the transaction.

    Returns:
      True if the transaction and associations were inserted successfully, False otherwise.
    """
    txn_id = self.transactions.insert_transaction(txn_hash, ts, json_data)
    if not txn_id:
        # print("usefull data")
        return False
    for wallet in wallet_hashes:
      #for the sake of not quering the api more than needed
      wallet_json_data = self.wallets.get_wallet_info(wallet)
      if not wallet_json_data:
        wallet_json_data = self.btc_api.get_wallet(wallet) 
      wallet_id = self.wallets.insert_wallet(wallet, wallet_json_data)
      if not wallet_id:
          # print("usefull data")
          return False
      #finally insert to relationship db
      linking_data = {'txn_id': txn_id, 'wallet_id': wallet_id, 'ts': ts}
      if not self.txn_wallets.insert_txn_wallet_pair(linking_data):
          return False  # Abort on any insert failure
    return True
  def insert_wallet(self, wallet_hash, json_data, txn_hashes):
    """
    Inserts a wallet and its associated tnxs.

    Args:
      wallet_hash: The hash of the transaction.
      json_data: The raw JSON data retrieved from the Blockchain.info API.
      txn_hashes: A list of wallet hash strings involved in the transaction.

    Returns:
      True if the transaction and associations were inserted successfully, False otherwise.
    """
    wallet_id = self.wallets.insert_wallet(wallet_hash, json_data)
    if not wallet_id:
      # print("usefull data")
      return False
    for txn in txn_hashes:
      txn_json_data = self.transactions.get_transaction_json(txn)
      if not txn_json_data:
        txn_json_data = self.btc_api.get_transaction(txn)
        
      ts = txn_json_data['time']
      txn_id = self.transactions.insert_transaction(txn, ts, txn_json_data)
      if not txn_id:
        # print("usefull data")
        return False
      #finally insert to relationship db
      linking_data = {'txn_id': txn_id, 'wallet_id': wallet_id, 'ts': ts}
      if not self.txn_wallets.insert_txn_wallet_pair(linking_data):
          return False  # Abort on any insert failure
    return True
      
  def get_transaction_json(self, txn_hash):
    """
    Retrieves the JSON data for a specific transaction.

    Args:
      txn_hash: The hash of the transaction.

    Returns:
      The raw JSON data for the transaction or None if not found.
    """
    return self.transactions.get_transaction_json(txn_hash)
  def get_wallet_info(self,wallet_hash):
    """
    Retrieves the JSON data for a specific transaction.

    Args:
      wallet_hash: The hash of the transaction.

    Returns:
      The raw JSON data for the wallet or None if not found.
    """
    return self.wallets.get_wallet_info(wallet_hash)
  
  def get_txns_from_wallet(self, wallet_hash):
    """
    Retrieves a list of transaction hashes associated with a specific wallet.

    Args:
      wallet_hash: The hash of the wallet.

    Returns:
      A list of transaction hash strings or None if no associations found.
    """
    return self.txn_wallets.get_transactions_for_wallet(wallet_hash)
  def get_wallets_from_txn(self, txn_hash):
    """
    Retrieves a list of transaction hashes associated with a specific wallet.

    Args:
      wallet_hash: The hash of the wallet.

    Returns:
      A list of transaction hash strings or None if no associations found.
    """
    #get txn id 
    
    return self.txn_wallets.get_wallets_for_transaction(txn_hash)
  # Similar methods for wallets and transaction-wallet associations (optional)
  def retrive_txn_json(self, txn_hash):
    """
    Retrive json data from db first and if it cant find the tx it will reach to the api
    
    Args:
        txn_hash: the hash of the txn
    
    Returns:
    json dict: json like dict containing the json obj
    """
    txn_data = self.get_transaction_json(txn_hash)
    if not txn_data:
        #first time seeing this txn
        txn_data = self.btc_api.get_transaction(txn_hash=txn_hash)
        relevant_wallets = self.extract_wallets_from_txn_json(txn_data)
        self.insert_transaction(txn_hash, txn_data['time'],txn_data, relevant_wallets)
    return txn_data
  def retrive_wallet_json(self, wallet_hash):
    """
    Retrive json data from db first and if it cant find the wallet it will reach to the api
    
    Args:
        wallet_hash: the hash of the txn
    
    Returns:
    json dict: json like dict containing the json obj
    """
    wallet_data = self.get_wallet_info(wallet_hash)
    if not wallet_data:
        #first time seeing this txn
        wallet_data = self.btc_api.get_wallet(wallet_hash)
        relevant_txns = self.extract_txns_from_wallet_json(wallet_data)
        self.insert_wallet(wallet_hash,wallet_data,relevant_txns)
    return wallet_data
   
  def close_connections(self):
    self.transactions.close()
    self.wallets.close()
    self.txn_wallets.close()
    