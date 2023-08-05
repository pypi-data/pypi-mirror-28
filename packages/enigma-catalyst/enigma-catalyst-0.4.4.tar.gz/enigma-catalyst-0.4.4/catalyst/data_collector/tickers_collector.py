import os

import pandas as pd
from logbook import Logger
from six import itervalues

from catalyst.constants import LOG_LEVEL
from catalyst.exchange.utils.exchange_utils import get_catalyst_symbol, \
    save_asset_data
from catalyst.exchange.utils.factory import find_exchanges
from catalyst.utils.paths import ensure_directory

log = Logger('TickersCollector', level=LOG_LEVEL)

DATADIR = '/Users/fredfortier/.catalyst-data/exchanges'
ensure_directory(DATADIR)


class TickersCollector:
    def __init__(self, exchanges):
        self.bar_count = 500
        self.exchanges = exchanges

    def __call__(self, exchange_name):
        log.info('scanning tickers for {}'.format(exchange_name))
        exchange = next(
            (exchange for exchange in \
             self.exchanges if exchange.name == exchange_name)
            , None
        )

        try:
            exchange.init()

            exchange_assets = exchange.get_assets()

            tickers = exchange.tickers(exchange_assets)
            all_tickers = list(itervalues(tickers))

            ticks = []
            for ticker in all_tickers:
                ticks.append(dict(
                    ask=ticker['ask'],
                    bid=ticker['bid'],
                    volume=ticker['volume'],
                    last_traded=ticker['last_traded'],
                    symbol=get_catalyst_symbol(ticker['symbol']),
                ))

            df = pd.DataFrame(ticks)
            df.set_index(
                ['symbol', 'last_traded'],
                drop=True,
                inplace=True,
            )
            log.debug('saving tickers')

            now = pd.Timestamp.utcnow()
            timestr = now.strftime('%Y%m')
            exchange_folder = os.path.join(
                DATADIR, exchange.name, timestr, 'tickers'
            )
            ensure_directory(exchange_folder)

            save_asset_data(exchange_folder, df)

        except Exception as e:
            log.warn(
                'unable to fetch tickers for {}: {}'.format(
                    exchange.name, e
                )
            )


if __name__ == '__main__':
    exchanges = find_exchanges(features=['fetchTickers'])
    collector = TickersCollector(exchanges)

    exchange_names = [exchange.name for exchange in exchanges]

    while True:
        for exchange_name in exchange_names:
            collector(exchange_name)
