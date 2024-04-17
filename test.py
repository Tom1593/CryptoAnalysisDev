from Database.DBService import DBService
from Api.wrappers.ApiWrapper import ApiWrapper

def main():
    dbs = DBService()
    api = ApiWrapper().get_wrapper()
    
    wallet_hash1 = "bc1p2wu5pcrv6gkawtx76caazkq95sjnu34rw6chy5vnfrzrhm9ms65slznr6j"
    txn_hash = "6bdb58b03488af492bb22f038908bac61a46533fbab485cee62e2d73889a8157"
    json_data = dbs.retrive_txn_json(txn_hash)
    wallets = dbs.extract_wallets_from_txn_json(json_data)
    dbs.insert_transaction(txn_hash,json_data['time'],json_data,wallets)
    if dbs.transactions.get_transaction(txn_hash):
        print("yay")
if __name__ == "__main__":
    main()