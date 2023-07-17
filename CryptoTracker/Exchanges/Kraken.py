import keys
import globalvar

from packages.kraken.exceptions import KrakenException
from packages.kraken.base_api import KrakenBaseSpotAPI, defined, ensure_string
from packages.kraken.spot import Trade


class Kraken:
    def __init__(self, glv):
        self.glv = glv
        self.client = None

    def get_client(self):
        if self.client is not None:
            return self.client

        if globalvar.get_ip() == globalvar.IP_WORK:
            return Trade(key=keys.KEY_KRAKEN_NONE)
        else:
            return Trade(key=keys.KEY_KRAKEN_TRADE)

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

    async def create_order(self, order_data):

        self.client.create_order(
            ordertype=order_data,
            side=order_data,
            pair=order_data['pair'],
            volume=order_data['amount'],
            validate=order_data['validate']
        )
