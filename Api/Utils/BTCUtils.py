
class BTCUtils:
    def extract_transaction_data(txn_obj):
        """
        Returns the required data from a transaction dict/json
    
        Args:
            txn_obj: txn data object from the Blockchain.info api representing 1 txn
        
        Returns:
            A tuple containing four lists:
                - input_hashes: A list of strings representing input transaction hashes.
                - output_hashes: A list of strings representing output transaction hashes (empty in this case).
                - input_amounts: A list of integers representing input transaction amounts in Satoshis.
                - output_amounts: A list of integers representing output transaction amounts in Satoshis.
        """
        inputs = {}
        outputs = {}

        for sender_entry in txn_obj['inputs']:
            inner_entry = sender_entry['prev_out']
            if inputs.get(inner_entry['addr']):
                inputs[inner_entry['addr']] += inner_entry['value']
            else:
                inputs[inner_entry['addr']] = inner_entry['value']
        for receiver_entry in txn_obj['out']:
            if outputs.get(receiver_entry['addr']):
                outputs[receiver_entry['addr']] += receiver_entry['value']
            else:
                outputs[receiver_entry['addr']] = receiver_entry['value']
        #transorme to lists
        input_hashes = [hash for hash in inputs]
        output_hashes = [hash for hash in outputs]
        input_amounts = [inputs[hash] for hash in inputs]
        output_amounts = [outputs[hash] for hash in outputs]
        return input_hashes, output_hashes, input_amounts, output_amounts
    def filter_transactions_by_timestamp(transactions, reference_timestamp, amount_transfered, original_txn_hash, later=True,):
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
            # Extract the timestamp and amount from the transaction data (replace with your keys)
            txn_timestamp = txn.get("time", 0)
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