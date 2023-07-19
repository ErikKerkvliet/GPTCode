import json
import keys

import globalvar

from packages.bitpanda.BitpandaClient import BitpandaClient
from packages.bitpanda.enums import OrderSide
from packages.bitpanda.Pair import Pair
from Exceptions import CoinIndexNotFoundException, CurrencyIndexNotFoundException
import http.client

import tracemalloc
import asyncio


class Bitpanda:

    def __init__(self, glv):
        self.glv = glv
        self.client = None
        tracemalloc.start()
        self.instruments = {}
        self.response = {}

    def get_client(self):
        if self.client is not None:
            return self.client

        if globalvar.get_ip() == globalvar.IP_WORK:
            return BitpandaClient(keys.KEY_NON_PRO)
        else:
            return BitpandaClient(keys.KEY_TRADE)

    async def close_client(self):
        if not self.client:
            return

        await self.client.close()
        self.client = None

    def ticker(self, coin='ALL', currency='ALL'):
        data = None
        crypto_codes = []

        if globalvar.get_ip() == globalvar.IP_HOME:
            loop = asyncio.get_event_loop()
            response = loop.run_until_complete(self.get_client().get_account_balances())
            response_data = response['response']['balances']

            for crypto in response_data:
                crypto_codes.append(crypto['currency_code'])

        connection = http.client.HTTPSConnection("api.bitpanda.com")
        while data is None:
            try:
                headers = {'Accept': "application/json"}

                connection.request("GET", "/v1/ticker", headers=headers)

                response = connection.getresponse()
                data = response.read()
            except http.client.NotConnected:
                print('Exception: disconnected. \n Reconnect')
                connection = http.client.HTTPSConnection("api.bitpanda.com")
                continue
            except http.client.HTTPException:
                print('Exception: HTTP Exception. \n Reconnect')
                connection = http.client.HTTPSConnection("api.bitpanda.com")
                continue

        response_data = json.loads(data.decode("utf-8"))

        if not crypto_codes:
            wallet = response_data
        else:
            wallet = {}
            for crypto in response_data.keys():
                if crypto in crypto_codes:
                    wallet[crypto] = response_data[crypto]

        if coin != 'ALL' and coin not in wallet.keys():
            raise CoinIndexNotFoundException

        if coin == 'ALL' and currency != 'ALL':
            coins_data = {}
            for coin in wallet.keys():
                coins_data[coin] = {}
                for currency_code in wallet[coin].keys():
                    coins_data[coin][currency_code] = float(wallet[coin][currency_code])
            return coins_data

        if coin == 'ALL':
            return wallet

        if currency not in wallet[coin]:
            raise CurrencyIndexNotFoundException

        if currency == 'ALL':
            return wallet[coin]

        return float(wallet[coin][currency])

    async def get_balances(self, coin='all'):
        response = await self.get_client().get_account_balances()

        if coin == 'all':
            return response['response']['balances']
        return response['response']['balances'][coin]

    async def sell(self, crypto):
        pair = Pair(crypto.code, globalvar.DEFAULT_CURRENCIES[0])

        # - 0.00036 BTC
        # + 10.02 EUR
        if globalvar.get_ip() == globalvar.IP_HOME:
            precision = crypto.instrument['amount_precision']
            trade_amount = round(crypto.amount, precision)
        else:
            trade_amount = round(crypto.amount, 5)

        order_data = {
            'pair': pair,
            'exchange_type': OrderSide.SELL,
            'amount': trade_amount,
            'crypto': crypto,
        }

        await self.create_order(order_data)

        crypto.profit += crypto.rate - crypto.buy_rate
        crypto.profit_euro += globalvar.BUY_AMOUNT * (crypto.rate / crypto.buy_rate) - globalvar.BUY_AMOUNT

        crypto.amount -= trade_amount
        crypto.amount_euro = crypto.amount / crypto.rate if crypto.amount > 0 else 0

        crypto.sells += 1
        crypto.position = 0

    async def buy(self, crypto, amount=None):
        rate = self.ticker(crypto.code, globalvar.DEFAULT_CURRENCIES[0])

        if not amount:
            amount = crypto.amount

        pair = Pair(crypto.code, globalvar.DEFAULT_CURRENCIES[0])

        if globalvar.get_ip() == globalvar.IP_HOME:
            precision = crypto.instrument['amount_precision']
            trade_amount = round(amount, precision)
        else:
            trade_amount = round(amount, 5)

        # BTC_EURO
        # + 0.00039 BTC
        # - 10 EUR
        order_data = {
            'pair': pair,
            'exchange_type': OrderSide.BUY,
            'amount': trade_amount,
            'crypto': crypto,
        }

        await self.create_order(order_data)

        await self.client.close()

        crypto.amount_euro += trade_amount / crypto.buy_rate

        crypto.buy_rate = crypto.rate
        crypto.buy_rate_euro = globalvar.BUY_AMOUNT / crypto.rate
        crypto.amount += globalvar.BUY_AMOUNT

        self.response['rate'] = float(rate)
        self.response['amount_euro'] = crypto.amount / crypto.rate

        return self.response

    def get_instrument(self, crypto='ALL'):
        if self.instruments:
            return self.instruments

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self.get_client().get_instruments())

        # self.client.close()

        for instrument in response['response']:
            self.instruments[instrument['base']['code']] = {
                'state': instrument['state'],
                'code': instrument['base']['code'],
                'precision': int(instrument['base']['precision']),
                'amount_precision': int(instrument['amount_precision']),
                'market_precision': int(instrument['market_precision']),
                'min_size': float(instrument['min_size']),
            }
        # print(sorted(list(self.instruments)))

        if crypto == 'ALL':
            return self.instruments

        return self.instruments[crypto]

    # UNI , EURO Koop 2 UNI voor ? EURO
    # side = OrderSide('BUY')
    # pair = Pair('UNI', 'EUR')
    # response = await client.create_market_order(pair, OrderSide.BUY, '2')
    # print(json.dumps(response['response']))
    # UNI , EUR sell 2 UNI voor ? EURO
    # await client.close()
    async def create_order(self, order_data) -> dict:
        amount = f'{float(order_data["amount"]):.8f}'

        number = (order_data['crypto'].amount / order_data['crypto'].rate) if order_data["exchange_type"] == 'SELL' else \
            globalvar.BUY_AMOUNT * float(((order_data['crypto'].rate / order_data['crypto'].buy_rate * 100 + 1) / 100))
        amount_euro = f"{float(number):.8f}"
        print(f'Type: {order_data["exchange_type"]}, Pair: {order_data["pair"]}, Amount: {amount}, Amount €: {amount_euro}')

        if globalvar.STATE == globalvar.STATE_DEVELOPMENT or globalvar.get_ip() == globalvar.IP_WORK:
            self.response = {
                'code': order_data['pair'],
                'amount': order_data['amount'],
            }
            return self.response
        #
        # if globalvar.STATE is globalvar.STATE_PRODUCTION:
        #     print('NOOOOO !!!!!!!!!!!!!!!!!!!')
        #     exit()
        return await self.get_client().create_market_order(
            order_data['pair'],
            order_data['exchange_type'],
            order_data['amount']
        )