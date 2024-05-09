#for when well implement eth
from .BTCWrapper import BTCWrapper
from .ETHWrapper import ETHWrapper
from Enumerators.BlockChainTypeEnum import BlockchainType

class ApiWrapper:
  def __init__(self):
      self.btc_api = BTCWrapper()
      self.eth_api = ETHWrapper()
      
  def get_wrapper(self,Coin:BlockchainType):
    if Coin == BlockchainType.BTC:
        return self.btc_api
    elif Coin == BlockchainType.ETH:
        return self.eth_api
    
  def get_transaction(self, txn_hash, Coin:BlockchainType):
    if Coin == BlockchainType.BTC:
        return self.btc_api.get_transaction(txn_hash)
    elif Coin == BlockchainType.ETH:
        json_data = self.eth_api.get_transaction(txn_hash)
        block_data = self.eth_api.get_block_by_number(json_data['blockNumber'])
        json_data['time'] = int(block_data['result']['timestamp'],16) #convert from hex to standart unix timestamp like in blockchain.info
        return json_data
        
    
  def get_wallet(self, wallet_hash, Coin:BlockchainType):
    if Coin == BlockchainType.BTC:
        return self.btc_api.get_wallet(wallet_hash)
    elif Coin == BlockchainType.ETH:
        return self.eth_api.get_wallet(wallet_hash)