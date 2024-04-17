# we get a txn -> get relevant wallets-> for each wallet explore -> build graph -> explore using api repeate
from Database.DBService import DBService
from Api.wrappers.ApiWrapper import ApiWrapper
from DataProcessing.TxnAnalysis import TxnAnalysis
from DataProcessing.Utils.GraphUtils import GraphUtils

def main():
    dbs = DBService()
    api = ApiWrapper().get_wrapper()
    analyzer = TxnAnalysis(dbs)
    
    txn_hash = "49595f288ea3de11fec0f12923d198370f1b2bb405634b3ac45d3662a4aeb332"
    txn_hash1 = "6bdb58b03488af492bb22f038908bac61a46533fbab485cee62e2d73889a8157"
    graph = analyzer.analyze_transaction(txn_hash)
    GraphUtils.create_graph(graph)
    
if __name__ == "__main__":
    main()
