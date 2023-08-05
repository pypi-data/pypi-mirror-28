"""
https://api.itbit.com/docs
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.api.REST import ItbitREST
from bitex.utils import return_api_response
from bitex.formatters.itbit import itbtFormatter as fmt

# Init Logging Facilities
log = logging.getLogger(__name__)


class ItBit(ItbitREST):
    def __init__(self, key='', secret='', key_file=''):
        super(ItbitREST, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)

    def public_query(self, endpoint, **kwargs):
        return self.query('GET', 'markets/' + endpoint, **kwargs)

    def private_query(self, endpoint, **kwargs):
        return self.query('POST', endpoint, authenticate=True, **kwargs)

    """
    BitEx Standardized Methods
    """

    @return_api_response(fmt.ticker)
    def ticker(self, pair, **kwargs):
        q = {'pair': pair}
        q.update(kwargs)
        return self.public_query('%s/ticker' % pair, params=q)

    @return_api_response(fmt.order_book)
    def order_book(self, pair, **kwargs):
        q = {'pair': pair}
        q.update(kwargs)
        return self.public_query('%s/order_book' % pair, params=q)

    @return_api_response(fmt.trades)
    def trades(self, pair, **kwargs):
        q = {'pair': pair}
        q.update(kwargs)
        return self.public_query('%s/trades' % pair, params=q)

    @return_api_response(fmt.order)
    def bid(self, pair, price, size, **kwargs):
        wallet_id = kwargs.pop('wallet')
        q = {'side': 'buy', 'type': 'limit', 'amount': size, 'price': price,
             'instrument': pair}
        q.update(kwargs)
        return self.private_query('wallets/%s/orders' % wallet_id, params=q)

    @return_api_response(fmt.order)
    def ask(self, pair, price, size, **kwargs):
        wallet_id = kwargs.pop('wallet')
        q = {'side': 'buy', 'type': 'limit', 'amount': size, 'price': price,
             'instrument': pair}
        q.update(kwargs)
        return self.private_query('wallets/%s/orders' % wallet_id, params=q)

    @return_api_response(fmt.cancel)
    def cancel_order(self, order_id, all=False, **kwargs):
        raise NotImplementedError()

    @return_api_response(fmt.order_status)
    def order(self, order_id, **kwargs):
        wallet_id = kwargs.pop('wallet_id')
        return self.private_query('wallets/%s/orders/%s' % (wallet_id, order_id),
                                  params=kwargs)

    @return_api_response(fmt.balance)
    def balance(self, **kwargs):
        raise NotImplementedError()

    @return_api_response(fmt.withdraw)
    def withdraw(self, size, tar_addr, **kwargs):
        wallet_id = kwargs.pop('wallet_id')
        q = {'address': tar_addr, 'amount': size}
        return self.private_query('wallets/%s/cryptocurrency_withdrawals' % wallet_id,
                                  params=q)

    @return_api_response(fmt.deposit)
    def deposit_address(self, **kwargs):
        wallet_id = kwargs.pop('wallet_id')
        return self.private_query('wallets/%s/cryptocurrency_deposits' % wallet_id,
                                  params=kwargs)

    """
    Exchange Specific Methods
    """
