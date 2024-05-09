import networkx as nx
from Api.Utils.ApiUtils import ApiUtils
# from Api.wrappers.BTCWrapper import BTCWrapper
from Database.DBService import DBService
from Enumerators.BlockChainTypeEnum import BlockchainType

class TxnAnalysis:
    def __init__(self, database_service : DBService):
        self.dbs = database_service
        
    def analyze_transaction(self, txn_hash, Coin:BlockchainType, depth=5):
        """
    Analyzes a Bitcoin transaction (given its hash) and builds a transaction graph using BFS.

    Args:
        txn_hash: The hash of the initial Bitcoin transaction.
        depth: Maximum depth for BFS exploration (optional).

    Returns:
        A NetworkX graph object representing the transaction network.
    """
    # we first need to deal with setting up the graph since the root node is a txn
    # but after that every node is a wallet and the txn are used to figure connections
        txn_data = self.dbs.retrive_txn_json(txn_hash,Coin)
        txn_time = txn_data['time']
        txn_in_out = ApiUtils.extract_transaction_data(txn_data,Coin)
        
        graph = nx.DiGraph()
        graph.add_node(txn_hash) #root node
        
        # Queue for BFS exploration
        queue = []
        current_depth = 0
        
        # graph set up
        for in_wallet,in_amount in zip(txn_in_out[0],txn_in_out[2]):
            graph.add_node(in_wallet)
            graph.add_edge(in_wallet,txn_hash,weight=in_amount/ApiUtils.format_price(Coin))
            prev_txns = ApiUtils.filter_transactions_by_timestamp(ApiUtils.extract_transactions_list_from_wallet_data(self.dbs.retrive_wallet_json(in_wallet,Coin)),
                                                                  txn_time,
                                                                  in_amount,
                                                                  txn_hash,
                                                                  later=False)
            queue.append((in_wallet,prev_txns))
            
        for out_wallet, out_amount in zip(txn_in_out[1],txn_in_out[3]):
            next_txns = ApiUtils.filter_transactions_by_timestamp(ApiUtils.extract_transactions_list_from_wallet_data(self.dbs.retrive_wallet_json(out_wallet,Coin)),
                                                                  txn_time,
                                                                  out_amount,
                                                                  txn_hash,
                                                                  later=True)
            graph.add_node(out_wallet)
            graph.add_edge(txn_hash,out_wallet,weight=out_amount/ApiUtils.format_price(Coin))
            queue.append((out_wallet,next_txns))
            
        
        while queue and current_depth < depth:
            #node,edges,weight
            current_wallet, txn_list = queue.pop(0)
            #add wallets nodes and connect them based on current wallet and txn
            for txn in txn_list:
                txn_in_out = ApiUtils.extract_transaction_data(txn,Coin)
                txn_time = txn['time']
                
                for in_wallet,in_amount in zip(txn_in_out[0],txn_in_out[2]):
                    if in_wallet not in graph:
                        graph.add_node(in_wallet)
                        
                    graph.add_edge(in_wallet,current_wallet,weight=in_amount/ApiUtils.format_price(Coin))
                    prev_txns = ApiUtils.filter_transactions_by_timestamp(ApiUtils.extract_transactions_list_from_wallet_data(self.dbs.retrive_wallet_json(in_wallet,Coin)),
                                                                          txn_time,
                                                                          in_amount,
                                                                          current_wallet,
                                                                          later=False)
                    queue.append((in_wallet,prev_txns))
                    
                for out_wallet, out_amount in zip(txn_in_out[1],txn_in_out[3]):
                    if in_wallet not in graph:
                        graph.add_node(in_wallet)
                        
                    graph.add_node(out_wallet)
                    graph.add_edge(current_wallet,out_wallet,weight=out_amount/ApiUtils.format_price(Coin))
                    next_txns = ApiUtils.filter_transactions_by_timestamp(ApiUtils.extract_transactions_list_from_wallet_data(self.dbs.retrive_wallet_json(out_wallet,Coin)),
                                                                          txn_time,
                                                                          out_amount,
                                                                          current_wallet,
                                                                          later=True)
                    queue.append((out_wallet,next_txns))
                current_depth += 1
        return graph