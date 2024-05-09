from BTCUtils import BTCUtils
from ETHUtils import ETHUtils
from Enumerators.BlockChainTypeEnum import BlockchainType
class ApiUtils():
    def extract_transaction_data(txn_data, Coin:BlockchainType):
        """
        intermidiate function to use the correct follow up proceess regarding the correct coin type

        Args:
        txn_data: transaction json data.
    
        Returns:
            the return value from the correct function in this case tuple with 4 lists
        """
        if Coin == BlockchainType.BTC:
            return BTCUtils.extract_transaction_data(txn_data)
        elif Coin == BlockchainType.ETH:
            return ETHUtils.extract_transaction_data(txn_data)
        
    def filter_transactions_by_timestamp(transactions, reference_timestamp, amount_transfered, original_txn_hash, Coin, later):
        """
        intermidiate function to use the correct follow up proceess regarding the correct coin type

        Args:
        txn_data: transaction json data.
    
        Returns:
            the return value from the correct function in this case a list containing transactions that meet the filtering criteria.
        """
        if Coin == BlockchainType.BTC:
            return BTCUtils.filter_transactions_by_timestamp(transactions,
                                                             reference_timestamp,
                                                             amount_transfered,
                                                             original_txn_hash,
                                                             later)
        elif Coin == BlockchainType.ETH:
            return ETHUtils.filter_transactions_by_timestamp(transactions,
                                                             reference_timestamp,
                                                             amount_transfered,
                                                             original_txn_hash,
                                                             later)
    
    def format_price(Coin:BlockchainType):
        if Coin == BlockchainType.BTC:
            return 1e8
        elif Coin == BlockchainType.ETH:
            return 1e18
    
    def extract_transactions_list_from_wallet_data(wallet_json,Coin:BlockchainType):
        if Coin == BlockchainType.BTC:
            return wallet_json['txs']
        elif Coin == BlockchainType.ETH:
            return wallet_json