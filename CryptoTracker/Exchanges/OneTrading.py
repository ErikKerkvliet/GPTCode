import tracemalloc

import globalvar
from CostHandler import CostHandler


class OneTrading:
    def __init__(self, glv):
        self.glv = glv
        self.client = None
        self.user = None
        self.times = 0
        self.pairs = self.asset_pairs()
        self.cost_handler = CostHandler()

    def asset_pairs(self, crypto_code=None):
        return self

    def ticker(self, crypto_code=None, wallet=None) -> dict:
        return {}

    def start_transaction(self, crypto, side):
        pass

    @staticmethod
    def get_balance_euro() -> float:
        return 0.0
