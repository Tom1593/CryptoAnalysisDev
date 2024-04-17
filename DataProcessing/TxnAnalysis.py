import networkx as nx
from Api.Utils.BTCUtils import BTCUtils
from Api.wrappers.BTCWrapper import BTCWrapper
from Database.DBService import DBService

class TxnAnalysis:
    def __init__(self, database_service : DBService):
        self.dbs = database_service
        
    def analyze_transaction(self, txn_hash,depth=5):
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
        txn_data = self.dbs.retrive_txn_json(txn_hash)
        txn_time = txn_data['time']
        txn_in_out = BTCUtils.extract_transaction_data(txn_data)
        
        graph = nx.DiGraph()
        graph.add_node(txn_hash) #root node
        
        # Queue for BFS exploration
        queue = []
        current_depth = 0
        
        # graph set up
        for in_wallet,in_amount in zip(txn_in_out[0],txn_in_out[2]):
            graph.add_node(in_wallet)
            graph.add_edge(in_wallet,txn_hash,weight=in_amount/1e8)
            prev_txns = BTCUtils.filter_transactions_by_timestamp(self.dbs.retrive_wallet_json(in_wallet)['txs'], txn_time, in_amount, txn_hash, later=False)
            queue.append((in_wallet,prev_txns))
            
        for out_wallet, out_amount in zip(txn_in_out[1],txn_in_out[3]):
            next_txns = BTCUtils.filter_transactions_by_timestamp(self.dbs.retrive_wallet_json(out_wallet)['txs'], txn_time,out_amount, txn_hash, later=True)
            graph.add_node(out_wallet)
            graph.add_edge(txn_hash,out_wallet,weight=out_amount/1e8)
            queue.append((out_wallet,next_txns))
            
        
        while queue and current_depth < depth:
            #node,edges,weight
            current_wallet, txn_list = queue.pop(0)
            #add wallets nodes and connect them based on current wallet and txn
            for txn in txn_list:
                txn_in_out = BTCUtils.extract_transaction_data(txn)
                txn_time = txn['time']
                
                for in_wallet,in_amount in zip(txn_in_out[0],txn_in_out[2]):
                    if in_wallet not in graph:
                        graph.add_node(in_wallet)
                        
                    graph.add_edge(in_wallet,current_wallet,weight=in_amount/1e8)
                    prev_txns = BTCUtils.filter_transactions_by_timestamp(self.dbs.retrive_wallet_json(in_wallet)['txs'], txn_time, in_amount, current_wallet, later=False)
                    queue.append((in_wallet,prev_txns))
                    
                for out_wallet, out_amount in zip(txn_in_out[1],txn_in_out[3]):
                    if in_wallet not in graph:
                        graph.add_node(in_wallet)
                        
                    graph.add_node(out_wallet)
                    graph.add_edge(current_wallet,out_wallet,weight=out_amount/1e8)
                    next_txns = BTCUtils.filter_transactions_by_timestamp(self.dbs.retrive_wallet_json(out_wallet)['txs'], txn_time,out_amount, current_wallet, later=True)
                    queue.append((out_wallet,next_txns))
                current_depth += 1
        return graph