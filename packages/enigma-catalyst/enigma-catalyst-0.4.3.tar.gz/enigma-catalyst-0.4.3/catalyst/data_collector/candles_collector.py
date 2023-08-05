import os
from datetime import timedelta
from time import sleep

import pandas as pd
from logbook import Logger

from catalyst.constants import LOG_LEVEL
from catalyst.exchange.exchange_errors import ExchangeRequestError
from catalyst.exchange.utils.bundle_utils import get_start_dt
from catalyst.exchange.utils.factory import find_exchanges
from catalyst.utils.paths import ensure_directory

log = Logger('CandlesCollector', level=LOG_LEVEL)

DATADIR = '/Users/fredfortier/.catalyst-data/exchanges'
ensure_directory(DATADIR)


class CandlesCollector:
    def __init__(self, exchanges):
        self.bar_count = 200
        self.exchanges = exchanges

    def _get_candles(self, exchange, freq, assets, bar_count, start_dt,
                     attempt=0):
        try:
            candles = exchange.get_candles(
                freq=freq,
                assets=assets,
                bar_count=bar_count,
                start_dt=start_dt,
            )
            return candles

        except ExchangeRequestError as e:
            log.warn(
                'unable to fetch candles on attempt {} {}'.format(attempt, e)
            )
            if attempt < 10:
                sleep(5)
                return self._get_candles(
                    exchange=exchange,
                    freq=freq,
                    assets=assets,
                    bar_count=bar_count,
                    start_dt=start_dt,
                    attempt=attempt + 1
                )

            else:
                raise e

    def __call__(self, exchange_name):
        log.info('scanning ohlcv data for {}'.format(exchange_name))
        exchange = next(
            (exchange for exchange in \
             self.exchanges if exchange.name == exchange_name)
            , None
        )

        exchange.init()
        exchange_assets = exchange.get_assets()

        now = pd.Timestamp.utcnow().floor('1T')
        for asset in exchange_assets:
            end_dt = now

            more_bars = True
            while more_bars:
                log.info(
                    'fetching candles {} - {}'.format(
                        asset.symbol, end_dt
                    )
                )
                start_dt = get_start_dt(
                    end_dt, self.bar_count, 'minute'
                )
                try:
                    candles = self._get_candles(
                        exchange=exchange,
                        freq='1T',
                        assets=[asset],
                        bar_count=self.bar_count,
                        start_dt=start_dt,
                    )
                except Exception as e:
                    log.warn('skipping asset on error {}', format(e))
                    break

                # If an asset is no longer available at that date
                # it won't be in the candles collection so we burn it
                if asset not in candles or not candles[asset]:
                    log.info('reached the last candle, moving on '
                             'to the next asset')
                    break

                asset_candles = candles[asset]
                last_candle = asset_candles[-1]
                first_candle = asset_candles[0]

                # Adding a buffer because there are not always trades
                # every minutes. Some exchanges yeild candles only when
                # there is a trade.
                adj_end = end_dt + timedelta(minutes=1)
                if last_candle['last_traded'] > adj_end:
                    log.info('removing duplicate after end date')

                    for candle in asset_candles[:]:
                        if candle['last_traded'] > end_dt:
                            asset_candles.remove(candle)

                    if not asset_candles:
                        break

                adj_start = start_dt + timedelta(minutes=60)
                if first_candle['last_traded'] > adj_start:
                    log.info('start date lated than specified, reached'
                             ' the last candle')

                    more_bars = False

                df = pd.DataFrame(asset_candles)
                df.set_index(
                    'last_traded',
                    drop=True,
                    inplace=True,
                )
                df.sort_index(inplace=True, ascending=False)
                log.debug('saving candles')

                timestr = now.strftime('%Y%m')
                exchange_folder = os.path.join(
                    DATADIR, exchange.name, timestr, 'candles'
                )
                ensure_directory(exchange_folder)

                filename = os.path.join(
                    exchange_folder, '{}.csv'.format(asset.symbol)
                )
                if os.path.exists(filename):
                    print_headers = False

                else:
                    print_headers = True

                with open(filename, 'a') as f:
                    df.to_csv(
                        path_or_buf=f,
                        header=print_headers,
                        float_format='%.{}f'.format(asset.decimals),
                    )

                end_dt = asset_candles[0]['last_traded']


if __name__ == '__main__':
    exchanges = find_exchanges(features=['fetchOHLCV'])
    collector = CandlesCollector(exchanges)

    exchange_names = [exchange.name for exchange in exchanges]

    collector('bittrex')
    # while True:
    #     for exchange_name in exchange_names:
    #         collector(exchange_name)
