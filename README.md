in order to use this one would need to install python and venv
then create a new virual env and run pip install -r req.txt to install all required packages
after that you need to create a .env file if not present and set up the following env variables:
env_var:{
  ETHERSCAN_API_KEY = "api_key"

  BTC_TXN_DB = "db_name.db"
  BTC_WALLET_DB = "db_name.db"
  BTC_TXN_WALLET_RELATION_DB = "db_name.db"

  ETH_TXN_DB = "eth_txn.db"

  DB_FOLDER = ""Path to db storing folder"
}
then because this is a poc the hash needs to be inserted to the main.py file
to run this code you could run the main.py file
