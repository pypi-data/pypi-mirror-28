import hashlib
import hmac
import time

import requests

from pycrybittrex.core import urlutils
from pycrybittrex.core.bittrexbase import BittrexBase
from pycrybittrex.definitions import Scope


class Bittrex11(BittrexBase):
    def __sign(self, url):
        return hmac.new(self.api_secret.encode(), url.encode(), hashlib.sha512).hexdigest()

    def __query(self, path, params, scope):
        if scope == Scope.PRIVATE:
            params['apikey'] = self.api_key
            params['nonce'] = int(round(time.time()))

            full_url = '{0}{1}{2}'.format(self.base_url(), path, urlutils.url_params(params))
            headers = {'apisign': self.__sign(full_url)}
        else:
            full_url = '{0}public/{1}{2}'.format(self.base_url(), path, urlutils.url_params(params))
            headers = {}

        return requests.get(full_url, headers=headers).json()

    def __checked_query(self, path, params, scope):
        response = self.__query(path, params, scope)

        if not response["success"]:
            raise RuntimeError("Request failed with message {0}".format(response["message"]))

        return response["result"]

    def base_url(self):
        return "https://bittrex.com/api/v1.1/"

    def get_markets(self):
        return self.__checked_query('getmarkets', params={}, scope=Scope.PUBLIC)

    def get_currencies(self):
        return self.__checked_query('getcurrencies', params={}, scope=Scope.PUBLIC)

    def get_ticker(self):
        return self.__checked_query('getticker', params={}, scope=Scope.PUBLIC)

    def get_market_summaries(self):
        return self.__checked_query('getmarketsummaries', params={}, scope=Scope.PUBLIC)

    def get_market_summary(self, market):
        return self.__checked_query('getmarketsummary', params={'market': market}, scope=Scope.PUBLIC)

    def get_order_book(self, market, order_type):
        return self.__checked_query('getorderbook', params={'market': market,
                                                            'type': order_type}, scope=Scope.PUBLIC)

    def get_market_history(self, market):
        return self.__checked_query('getmarkethistory', params={'market': market}, scope=Scope.PUBLIC)

    def buy_limit(self, market, quantity, rate):
        return self.__checked_query('market/buylimit', params={'market': market,
                                                               'quantity': quantity,
                                                               'rate': rate}, scope=Scope.PRIVATE)

    def sell_limit(self, market, quantity, rate):
        return self.__checked_query('market/selllimit', params={'market': market,
                                                                'quantity': quantity,
                                                                'rate': rate}, scope=Scope.PRIVATE)

    def cancel(self, uuid):
        return self.__checked_query('market/cancel', params={'uuid': uuid}, scope=Scope.PRIVATE)

    def get_open_orders(self, market):
        return self.__checked_query('market/getopenorders', params={'market': market}, scope=Scope.PRIVATE)

    def get_balances(self):
        return self.__checked_query('account/getbalances', params={}, scope=Scope.PRIVATE)

    def get_balance(self, currency):
        return self.__checked_query('account/getbalance', params={'currency': currency}, scope=Scope.PRIVATE)

    def get_deposit_address(self, currency):
        return self.__checked_query('account/getdepositaddress', params={'currency': currency}, scope=Scope.PRIVATE)

    def withdraw(self, currency, quantity, address, payment_id):
        return self.__checked_query('account/withdraw', params={'currency': currency,
                                                                'quantity': quantity,
                                                                'address': address,
                                                                'paymentid': payment_id}, scope=Scope.PRIVATE)

    def get_order(self, uuid):
        return self.__checked_query('account/getorder', params={'uuid': uuid}, scope=Scope.PRIVATE)

    def get_order_history(self, market):
        return self.__checked_query('account/getorderhistory', params={'market': market}, scope=Scope.PRIVATE)

    def get_withdrawal_history(self, currency):
        return self.__checked_query('account/getwithdrawalhistory', params={'currency': currency}, scope=Scope.PRIVATE)

    def get_deposit_history(self, currency):
        return self.__checked_query('account/getdeposithistory', params={'currency': currency}, scope=Scope.PRIVATE)
