
class ETHUtils:
    def extract_transaction_data(txn_obj):
        """
        Returns the required data from a transaction dict/json
    
        Args:
            txn_obj: txn data object from the api interface representing 1 txn
        
        Returns:
            A tuple containing four lists:
                - input_hashes: A list of strings representing input transaction hashes.
                - output_hashes: A list of strings representing output transaction hashes (empty in this case).
                - input_amounts: A list of integers representing input transaction amounts in Satoshis.
                - output_amounts: A list of integers representing output transaction amounts in Satoshis.
                but they will each contain one element beacuse its eth txn
        """
        
        return (txn_obj['from'],txn_obj['to'],txn_obj['value'],txn_obj['value'])
    def filter_transactions_by_timestamp(transactions, reference_timestamp, amount_transfered, original_txn_hash, later=True):
        """
        Filters a list of transactions based on a reference timestamp and tracks sent/received amounts.

        Args:
            transactions: A list of dictionaries representing Bitcoin transactions.
            reference_timestamp: The reference timestamp (in Unix time) for filtering.
            later: Boolean flag indicating whether to filter for transactions later 
            (True) or earlier (False) than the reference timestamp (defaults to True).

        Returns:
            A new list containing transactions that meet the filtering criteria.
        """
        filtered_transactions = []
        total_amount = 0  # Track total sent/received amount (adjust sign based on later)
        for txn in transactions:
            if txn['hash'] == original_txn_hash:
                continue
            # Extract the timestamp and amount from the transaction data
            txn_timestamp = txn.get("timeStamp", 0)
            txn_amount = abs(txn['result'])

            if later and txn_timestamp > reference_timestamp and total_amount < amount_transfered:
                filtered_transactions.append(txn)
                total_amount += txn_amount  # Track total received amount
            elif not later and txn_timestamp < reference_timestamp and total_amount < amount_transfered: 
                filtered_transactions.append(txn)
                total_amount += txn_amount  # Track total sent amount
            # Stop filtering when total sent reaches the target amount (for earlier transactions)
            elif total_amount >= amount_transfered:
                break
        return filtered_transactions  