# -*- coding: utf-8 -*-

"""LPRPC abstract module."""
import os
import click
import bitcoin.rpc


class LPRPC:

    coins = ['BTC', 'KMD', 'MNZ']

    configs = {
        'BTC': '.bitcoin/bitcoin.conf',
        'MNZ': '.komodo/MNZ/MNZ.conf',
        'KMD': '.komodo/komodo.conf'
    }

    allowed_methods = [
        'getbalance',
        'is_sync'
    ]

    def __init__(self, home, method, coin=None):
        coin = coin.upper()
        if not coin or coin not in self.coins:
            raise Exception("No coin/unknown coin selected")
        self.coin = coin
        conf_file = os.path.join(home, self.configs[self.coin])
        self.proxy = bitcoin.rpc.Proxy(btc_conf_file=conf_file, timeout=2)

    def _call(self, method):
        try:
            response = self.proxy.call(method)
            return response
        except Exception as e:
            click.echo("ERROR:" + str(e))
            exit(1)

    def call(self, method):
        """
        Universal method for calling coin's RPC server.
        """
        # if method not in self.allowed_methods:
        #     click.echo("ERROR: Method unauthorized.")
        #     click.echo("HINT: authorized methods: %s" % (', ').join(self.allowed_methods))
        #     exit(1)
        internal_method =  getattr(self, method, None)
        if internal_method:
            response = internal_method()
        else:
            response = self._call(method)
            if response:
                click.echo(response)
        return response
    
    def getbalance(self):
        """
        Return coin's current balance.
        """
        balance = self._call('getbalance')
        balance = float(balance)
        click.echo(balance)
        return balance

    def is_sync(self):
        """
        Return:
        * 0 if the blockchain is synced.
        * 1 if the blockchain isn't synced.
        """
        blockchain_info = self._call('getblockchaininfo')
        if response and blockchain_info['blocks'] == blockchain_info['headers']:
            click.echo(0)
            exit(False)
        else:
            click.echo(1)
            exit(True)