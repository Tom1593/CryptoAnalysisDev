#for when well implement eth
from .BTCWrapper import BTCWrapper

class ApiWrapper:
  def __init__(self):
      self.btc_api = BTCWrapper()
  def get_wrapper(self):
      return self.btc_api