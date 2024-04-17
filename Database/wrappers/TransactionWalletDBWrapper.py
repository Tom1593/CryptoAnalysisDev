from .DatabaseWrapper import DatabaseWrapper

class TransactionWalletDB(DatabaseWrapper):
  """
  Wrapper class for interacting with the transaction_wallets table.
  """

  def __init__(self, db_path):
    super().__init__(db_path)
    self._table_name = 'Transaction_Wallet'  # Assuming 'Transaction_Wallet' table
    self._create_table()

  def _create_table(self):
    super()._create_table(self._table_name)

  def insert_txn_wallet_pair(self, linking_data):
      if super().get(self._table_name,{'txn_id': linking_data['txn_id'], 'wallet_id':linking_data['wallet_id']}):
          # print("duplicate entry")
          return True
      success = super().insert(self._table_name,linking_data)
      if not success:
        # print("couldnt insert")
        return False
      return True
      
  def get_wallets_for_transaction(self, txn_id):
    """
    Retrieves a list of wallet hashes associated with a specific transaction.

    Args:
      txn_hash: The hash of the transaction.

    Returns:
      A list of wallet hash strings or None if no associations found.
    """
    return super().get(self._table_name,{'txn_id': txn_id})

  def get_transactions_for_wallet(self, wallet_id):
    """
    Retrieves a list of transaction hashes associated with a specific wallet.

    Args:
      wallet_hash: The hash of the wallet.

    Returns:
      A list of transaction hash strings or None if no associations found.
    """
    return super().get(self._table_name,{'wallet_id': wallet_id})

  # You could define other methods for specific needs (e.g., delete wallet association)
