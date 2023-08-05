__author__ = 'Slavko Bojanic <slavkobojj@gmail.com>'
__version__ = '0.0.1'
__license__ = 'GPLv3'

"""

The foundations of this API were completely built upon from Peter Dyson's original implementation.

https://github.com/geekpete/
https://github.com/geekpete/py-coinspot-api/

His version has been un-updated for a few years now and I thought that I may as well try and continue maintaining it, seeing as he probably won't be. It is more or less the same for the time being, i'm simply trying to clean up the code and perhaps add some new features/improve upon those already existing ones.

"""

import hmac
import hashlib
import requests
import json

from time import time, strftime

"""

Changes from v1:

* Removed logging and debugging - an issue that the old API had was that it was very 'hacky', i've tried to make it as streamlined and as easy to understand as possible. If people do feel they need logging and debugging, they're always welcome to add it since this is open-source.

"""

class CoinSpot:
    """

    Default class variables.

    """

    API_key = ""
    API_secret = ""
    _endpoint = "https://www.coinspot.com.au"



    def __init__(self, key, secret):
        """

        In the original version of the py-coinspot-api, YAML / Environment variables were used to fetch API_key and API_secret.
        I thought that this was less secure than just initializing the object with the API_key and API_secret as parameters.

        Whilst this would make it more difficult for a newbie to use, lets be real, they probably won't be using this API ;P

        """

        self.API_key = key
        self.API_secret = secret



    def getSignedRequest(self, data):
        """

        Takes formatted JSon data and signs it with your secret key according to the HMAC-SHA512 method.

        :param data:
            The data which needs to be signed with SHA512, typically includes relevant post data and nonce value

        """
        return hmac.new(self.API_secret.encode('utf-8'), data.encode('utf-8'), hashlib.sha512).hexdigest()



    def request(self, path, requestData):
        """

        Send a request to the CoinSpot API endpoint.

        :param path:
            The address to append onto the endpoint url

        :param requestData:
            The required post data to make a valid post to the above specified URL

        :return:
            The JSon returned from the request

        """

        nonceValue = int(time()*102030) # Complex number which will never be less than the previous request (note: multiplied by 102030 so as to not conflict with any possible epoch time conversions which occur in the code... you never know...)

        requestData['nonce'] = nonceValue
        requestDataDumped = json.dumps(requestData, separators=(',', ':'))

        signedSecret = self.getSignedRequest(requestDataDumped)

        headers = {
            'Content-type': 'application/json',
            'Accept': 'text/plain',
            'key': self.API_key,
            'sign': signedSecret,
            'User-Agent': 'https://www.github.com/slavkobojanic/Python-CoinSpot-V2'
        }

        url = self._endpoint + path

        post = requests.post(url, data=requestDataDumped, headers=headers) # Request is sent
        print(post.json())



    def latestPrices(self):
        """

        TODO: For some reason this wouldn't work, and I couldn't figure out why for the life of me.

        Maybe something to do with it being a post request rather than a get?

        :return:
            All coin prices

        """

        return requests.get("https://www.coinspot.com.au/pubapi/latest").json()



    def listOpenOrders(self, cointype):
        """

        :param cointype:
            The type of coin.

        :return:
            Status (ok, error)
            All buy orders
            All sell orders

        """

        requestData = {
            'cointype': cointype
        }

        return self.request('/api/orders', requestData)



    def listOrderHistory(self, cointype):
        """

        :param cointype:
            The type of coin.

        :return:
            Status (ok, error).
            Last 1000 orders.

        """

        requestData = {
            'cointype': cointype
        }

        return self.request('/api/orders/history', requestData)



    def depositCoins(self, cointype):
        """

        :param cointype:
            The type of coin.

        :return:
            Status (ok, error).
            Wallet address.

        """

        requestData = {
            'cointype': cointype
        }

        return self.request('/api/my/coin/deposit', requestData)



    def sendCoins(self, cointype, address, amount):
        """

        :param cointype:
            The type of coin.

        :param address:
            The recipients wallet address.

        :param amount:
            The amount of -> COINS <- to send.

        :return:
            Status (ok, error)

        """

        if cointype.lower() == "ada":
            raise ValueError('Cardano ($ADA) is not supported yet with the CoinSpot API due to requiring a MEMO.id in the post, apologies.')

        requestData = {
            'cointype': cointype,
            'address': address,
            'amount': amount
        }

        return self.request('/api/my/coin/send', requestData)



    def quickBuyQuote(self, cointype, amount):
        """

        :param cointype:
            The type of coin.

        :param amount:
            The amount of -> COINS <- to buy.

        :return:
            Status (ok, error).
            Quote (rate per coin).
            Timeframe (estimated hours to wait for trade to complete, 0 = immediate trade).

        """

        requestData = {
            'cointype': cointype,
            'amount': amount
        }

        return self.request('/api/quote/buy', requestData)



    def quickSellQuote(self, cointype, amount):
        """

        :param cointype:
            The type of coin.

        :param amount:
            The amount of -> COINS <- to sell.

        :return:
            Status (ok, error).
            Quote (rate per coin).
            Timeframe (estimated hours to wait for trade to complete, 0 = immediate trade).

        """

        requestData = {
            'cointype': cointype,
            'amount': amount
        }

        return self.request('/api/quote/sell', requestData)



    def listMyBalances(self):
        """

        :return:
            Status (ok, error).
            All your balances

        """

        requestData = {}

        return self.request('/api/my/balances', requestData)



    def listMyOrders(self):
        """

        :return:
            Status (ok, error).
            All your buy orders.
            All your sell orders.

        """

        requestData = {}

        return self.request('/api/my/orders', requestData)



    def placeBuyOrder(self, cointype, amount, rate):
        """

        :param cointype:
            The type of coin.

        :param amount:
            The amount of coins you want to buy, maximum of 8 decimal places.

        :param rate:
            The rate in AUD you are willing to buy for, maximum of 6 decimal places.

        :return:
            Status (ok, error).

        """

        requestData = {
            'cointype': cointype,
            'amount': amount,
            'rate': rate
        }

        return self.request('/api/my/buy', requestData)



    def placeSellOrder(self, cointype, amount, rate):
        """

        :param cointype:
            The type of coin.

        :param amount:
            The amount of coins you want to sell, maximum of 8 decimal places.

        :param rate:
            The rate in AUD you are willing to sell for, maximum of 6 decimal places.

        :return:
            Status (ok, error).

        """

        requestData = {
            'cointype': cointype,
            'amount': amount,
            'rate': rate
        }

        return self.request('/api/my/sell', requestData)



    def cancelBuyOrder(self, id):
        """

        :param id:
            The id of the buy order you'd like to cancel

        :return:
            Status (ok, error)

        """

        requestData = {
            'id': id
        }

        return self.request('/api/my/buy/cancel')



    def cancelSellOrder(self, id):
        """

        :param id:
            The id of the sell order you'd like to cancel

        :return:
            Status (ok, error)

        """

        requestData = {
            'id': id
        }

        return self.request('/api/my/buy/cancel')
