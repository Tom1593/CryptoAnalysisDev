from .DatabaseWrapper import DatabaseWrapper  # Assuming database_wrapper.py in same directory
import json

class TransactionDB(DatabaseWrapper):
  """
  Wrapper class for interacting with the transaction database.
  """

  def __init__(self, db_path):
    super().__init__(db_path)
    self._table_name = 'Transactions'  # Assuming 'Transactions' table
    self._create_table()

  def _create_table(self):
    super()._create_table(self._table_name)

  def insert_transaction(self, txn_hash, ts, json_data) -> int|bool:
    """
    Inserts a new transaction entry into the database.

    Args:
      txn_hash: The hash of the transaction.
      json_data: The raw JSON data retrieved from the Blockchain.info API.
      wallet_hashes: A list of wallet hash strings involved in the transaction.

    Returns:
      txn_id if the transaction info was inserted successfully, False otherwise.
    """
    # duplicate key check logic (optional)
    dup = self.get(self._table_name, {'txn_hash': txn_hash})
    if dup:
      # print(entry exists)
      return dup[0][0]  # Already exists

    # Insert transaction data
    transaction_data = {
        'txn_hash': txn_hash,
        'ts': ts,
        'json_data': json.dumps(json_data),
    }
    txn_id = super().insert(self._table_name, transaction_data)
    if not txn_id:
      print(f"could not insert txn: {txn_hash}")
      return False
    # print(f"inserted txn {txn_hash}")
    return txn_id
  def get_transaction(self, txn_hash):
    """
    Retrieves the row data for a specific transaction.

    Args:
      txn_hash: The hash of the transaction.

    Returns:
      The raw data for the transaction or None if not found.
    """
    transaction = super().get(self._table_name,{'txn_hash': txn_hash})
    return transaction if transaction else None
  def get_transaction_json(self, txn_hash):
    """
    Retrieves the JSON data for a specific transaction.

    Args:
      txn_hash: The hash of the transaction.

    Returns:
      The raw JSON data for the transaction or None if not found.
    """
    transaction = super().get(self._table_name, {'txn_hash': txn_hash})
    if transaction:
      try:
        json_data = json.loads(transaction[0][3])
        return json_data
      except json.JSONDecodeError:
        print("Invalid JSON Data")
        return None
    else:
      return None

  def update_transaction(self, txn_hash, new_json_data):
    """
    Updates the JSON data for an existing transaction.

    Args:
      txn_hash: The hash of the transaction to update.
      new_json_data: The updated JSON data for the transaction.

    Returns:
      True if the transaction data was updated successfully, False otherwise.
    """
    transaction_data = {'json_data': new_json_data}
    return super().update(self._table_name, transaction_data, {'hash': txn_hash})

  def delete_transaction(self, txn_hash):
    """
    Deletes a transaction entry from the database.

    Args:
      txn_hash: The hash of the transaction to delete.

    Returns:
      True if the transaction was deleted successfully, False otherwise.
    """
    # Delete transaction-wallet associations first (optional for data integrity)
    # ... (consider deleting from transaction_wallets with matching transaction_hash)

    return super().delete(self._table_name, {'txn_hash': txn_hash})
