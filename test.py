from Database.DBService import DBService
from Api.wrappers.ApiWrapper import ApiWrapper,BlockchainType
from DataProcessing.TxnAnalysis import TxnAnalysis
from DataProcessing.Utils.GraphUtils import GraphUtils

def main():
    dbs = DBService()
    api_interface = ApiWrapper()
    analyzer = TxnAnalysis(dbs)
    # eth
    
    wallet_hash = "0xefcBF90f60e0714362D942a054e6B716983fEA2b"
    txn_hash = "0x2ce955a844d306882c429420c97511200854b88dc61d95076768834af7e630d2"
    block_number = "0xcf2420"
    json_data = api_interface.eth_api.get_transaction(txn_hash)
    # wallet_data = api_interface.eth_api.get_wallet(wallet_hash)
    # block_data = api_interface.eth_api.get_block_by_number(block_number)
    # time = int(block_data['result']['timestamp'],16)
    # data = dbs.retrive_txn_json(txn_hash,BlockchainType.ETH)
    # data = dbs.retrive_wallet_json(wallet_hash,BlockchainType.ETH)
    # txns = dbs.extract_txns_from_wallet_json(data,BlockchainType.ETH,limit=10)
    # print(f"eht is: {int(json_data['value'],16)/1e18}")
    
    
    # btc
    # wallet_hash1 = "bc1p2wu5pcrv6gkawtx76caazkq95sjnu34rw6chy5vnfrzrhm9ms65slznr6j"
    # txn_hash = "6bdb58b03488af492bb22f038908bac61a46533fbab485cee62e2d73889a8157"
    # json_data = dbs.retrive_txn_json(txn_hash)
    # wallets = dbs.extract_wallets_from_txn_json(json_data)
    # dbs.insert_transaction(txn_hash,json_data['time'],json_data,wallets)
    # if dbs.transactions.get_transaction(txn_hash):
    #     print("yay")
    
    #main test
    
    graph = analyzer.analyze_transaction(txn_hash,BlockchainType.ETH)
    GraphUtils.create_graph(graph)
    
    
if __name__ == "__main__":
    main()