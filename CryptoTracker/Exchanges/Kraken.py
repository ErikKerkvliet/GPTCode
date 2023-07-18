import keys
import globalvar

from packages.kraken.exceptions import KrakenException
from packages.kraken.base_api import KrakenBaseSpotAPI, defined, ensure_string
from packages.kraken.spot import Trade
from packages.kraken.spot import User


class Kraken:
    def __init__(self, glv):
        self.glv = glv
        self.client = None
        self.user = User(key=keys.KEY_KRAKEN_API, secret=keys.KEY_KRAKEN_PRIVATE)

    def get_client(self):
        if self.client is not None:
            return self.client
        return KrakenBaseSpotAPI(key=keys.KEY_KRAKEN_API)

    async def close_client(self):
        if not self.client:
            return

        await self.client.close()
        self.client = None

    async def buy(self, crypto):

        order_data = {
            'ordertype': 'market',
            'side': 'buy',
            'pair': '',
            'amount': crypto.amount,
            'validate': True  # Test variable
        }

        if not globalvar.TEST:
            order_data['validate'] = False

        await self.create_order(order_data)

    def sell(self, crypto):
        pass

    def get_balances(self):
        with self.user as user:
            balances = user.get_balances()

        for key in balances.keys():
            balance[key]
        return balances

    async def create_order(self, order_data):

        self.client.create_order(
            ordertype=order_data,
            side=order_data,
            pair=order_data['pair'],
            volume=order_data['amount'],
            validate=order_data['validate']
        )
