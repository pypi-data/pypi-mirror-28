# -*- coding: utf-8 -*-

"""Liquidity Provider Monitoring CLI"""
from .rpc import LPRPC
import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--coin', '-c', help="Coin selection: %s" % ('|').join(LPRPC.coins))
@click.option('--home', '-H',   type=click.Path(exists=True,file_okay=False),
                                default="/home/chef",
                                help="Sets home directory which contains <coins>.conf files")
@click.argument('method')
def main(args=None, **kwargs):
    """Liquidity Provider Monitoring CLI"""
    LPRPC(**kwargs).call(kwargs['method'])

if __name__ == "__main__":
    main()
