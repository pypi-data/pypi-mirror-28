import time

import boto3
import numpy as np
import pandas as pd
import requests
from logbook import Logger, DEBUG

from catalyst import run_algorithm
from catalyst.api import symbol, record
from catalyst.exchange.exchange_errors import SymbolNotFoundOnExchange
from catalyst.exchange.utils.stats_utils import get_pretty_stats

algo_namespace = 'arbitrage_poloniex_bitfinex_bittrex'

log = Logger(algo_namespace)
log.level = DEBUG

s3 = boto3.resource('s3')


def initialize(context):
    context.signals = []

    context.hourly_orderbook_data = []
    context.current_hour = None

    context.num_opportunities = 0
    context.max_percent = 0

    context.targets = dict()

    context.targets['eth_btc'] = \
        dict([(1, 1), (1.5, 1.1), (1.75, 1.2), (2, 1.5), (3, 2)])

    context.targets['ltc_btc'] = \
        dict([(2, 1.0), (5, 1.5), (10, 2.0), (40, 2.5), (60, 3.0)])

    context.targets['xmr_btc'] = \
        dict([(1, -1), (3, 1.5), (8, -1), (30, 2.5), (40, 3.0)])

    context.targets['omg_btc'] = \
        dict([(50, 1.0), (100, 1.5), (200, 2.0), (400, 2.5), (600, 3.0)])

    context.targets['neo_btc'] = \
        dict([(2, 1.0), (5, 1.5), (10, 2.0), (40, 2.5), (60, 3.0)])

    # context.targets['dash_btc'] = \
    #     dict([(1, 1.0), (2, 1.5), (4, 2.0), (8, 2.5), (12, 3.0)])

    context.targets['etc_btc'] = \
        dict([(1, 1.0), (3, 1.5), (8, 2.0), (30, 2.5), (40, 3.0)])
    #
    # context.targets['zec_btc'] = \
    #     dict([(1, 1.0), (2, 1.5), (4, 2.0), (8, 2.5), (12, 3.0)])

    context.targets['qtum_btc'] = \
        dict([(1, 1.0), (3, 1.5), (8, 2.0), (30, 2.5), (40, 3.0)])
    #
    # context.targets['lisk_btc'] = \
    #     dict([(50, 1.0), (100, 1.5), (200, 2.0), (400, 2.5), (600, 3.0)])
    #
    # context.targets['xlm_btc'] = \
    #     dict([(10000, 1.0), (20000, 1.5), (40000, 2.0), (80000, 2.5),
    #           (120000, 3.0)])
    #
    # context.targets['stem_btc'] = \
    #     dict([(10, 1.0), (30, 1.5), (80, 2.0), (300, 2.5), (400, 3.0)])
    #
    # context.targets['dcr_btc'] = \
    #     dict([(1, 1.0), (3, 1.5), (8, 2.0), (30, 2.5), (40, 3.0)])


def calculate_orderbook_totals(context, quantity, orderbooks):
    """
    Calculate the cost of the given asset.

    :param context:
    :param symbol:
    :param quantity:
    :param orderbooks:

    :return:
        A dictionary breaking down the cost by:
            exchange_name: str
                The name of the exchange

                    order_type: str
                        The type of orders (bids or asks)
    """
    totals = dict()

    for exchange_name in context.exchanges:
        orderbook = orderbooks[exchange_name]

        totals[exchange_name] = dict()

        if orderbook is None:
            totals[exchange_name]['bids'] = np.nan
            totals[exchange_name]['asks'] = np.nan

        else:
            for order_type in ['bids', 'asks']:
                entries = orderbook[order_type]

                index = 0
                total = 0
                remaining_quantity = quantity

                while remaining_quantity > 0:
                    try:
                        entry = entries[index]

                        entry_quantity = entry['quantity']

                        order_quantity = entry_quantity \
                            if entry_quantity <= remaining_quantity \
                            else remaining_quantity

                        remaining_quantity -= order_quantity

                        total += order_quantity * entry['rate']

                        index += 1
                    except Exception as e:
                        log.warn('order book error on {}, {}'.format(
                            exchange_name, e
                        ))
                        total = np.nan
                        break

                totals[exchange_name][order_type] = total

    return totals


def print_df(df):
    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('precision', 8)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)

    return df.to_string()


def is_opportunity(context, df, index, percent):
    index = df.index.values[index]

    target = context.targets[index[1]][index[2]]
    if percent > target:
        return True
    else:
        return False


def apply_opportunities(context, df):
    log.info('mapping opportunity signals')
    has_opportunity = False

    for column in df.columns:
        if 'percent' in column[1]:
            label = column[1]

            column_name = label.replace('percent', 'opportunity')

            df[(column[0], column_name)] = \
                [is_opportunity(context, df, idx, df.iloc[idx][column]) for idx
                 in range(len(df))]

            if df[(column[0], column_name)].any():
                has_opportunity = True

    return has_opportunity


def apply_orders(context, df):
    print('applying orders')
    exchanges = context.exchanges.keys()[:]

    while len(exchanges) > 0:
        source_exchange = exchanges.pop(0)

        for target_exchange in exchanges:
            label = '{}_{}'.format(source_exchange, target_exchange)
            order_label = '{}_order'.format(label)

            for ob_type in ['ask', 'bid']:
                opportunity_column = (
                    ob_type, '{}_opportunity'.format(label)
                )
                orders = []

                def calculate_order(row):
                    has_opportunity = row[opportunity_column]

                    value = None
                    if has_opportunity and len(orders) == 0:
                        exchanges = label.split('_')
                        source_exchange = exchanges[0]
                        target_exchange = exchanges[1]

                        if ob_type == 'ask':
                            value = 'buy {}: {}, sell {}: {}'.format(
                                source_exchange, row['ask', source_exchange],
                                target_exchange, row['bid', target_exchange]
                            )

                        elif ob_type == 'bid':
                            value = 'buy {}: {}, sell {}: {}'.format(
                                target_exchange, row['ask', source_exchange],
                                source_exchange, row['bid', target_exchange]
                            )

                        orders.append(value)

                    return value

                sorted_df = df.sort_index(
                    axis=0, level='quantity', ascending=False
                )
                df[ob_type, order_label] = sorted_df.apply(
                    calculate_order, axis=1
                )


def create_orderbook_panel(context, data):
    panel_date = pd.Timestamp.utcnow().floor('1 min')
    panel_hour = panel_date.floor('1H')

    if context.current_hour is None or panel_hour != context.current_hour:
        context.current_hour = panel_hour
        context.hourly_orderbook_data = []

    orderbook_data = []
    for pair_symbol in context.targets:
        orderbooks = dict()
        for exchange_name in context.exchanges:
            try:
                asset = symbol(pair_symbol, exchange_name)

                # TODO: add orderbook api interface
                exchange = context.exchanges[exchange_name]
                orderbooks[exchange_name] = exchange.get_orderbook(asset)

            except SymbolNotFoundOnExchange:
                orderbooks[exchange_name] = None

        for quantity in context.targets[pair_symbol]:

            orderbook_totals = \
                calculate_orderbook_totals(context, quantity, orderbooks)

            for exchange_name in orderbook_totals:
                order_types = orderbook_totals[exchange_name]

                spot_orderbook = dict(
                    date=panel_date,
                    pair_symbol=pair_symbol,
                    quantity=quantity,
                    exchange=exchange_name,
                    ask=order_types['asks'],
                    bid=order_types['bids']
                )

                orderbook_data.append(spot_orderbook)
                context.hourly_orderbook_data.append(spot_orderbook)

    orderbook_df = create_panel(context, orderbook_data)
    has_opportunity = apply_opportunities(context, orderbook_df)

    # TODO: place orders here

    apply_orders(context, orderbook_df)
    result = print_df(orderbook_df)
    print(result)

    if has_opportunity:
        context.num_opportunities += 1

        timestr = panel_date.strftime('%Y%m%d-%H%M%S')
        to_s3(orderbook_df, 'opportunities', timestr)
        send_email(orderbook_df)

    hourly_orderbook_df = create_panel(context, context.hourly_orderbook_data)
    apply_opportunities(context, hourly_orderbook_df)

    timestr = panel_hour.strftime('%Y%m%d-%H')
    to_s3(hourly_orderbook_df, 'hourly', timestr)


def create_panel(context, orderbook_data):
    orderbook_df = pd.DataFrame(orderbook_data)
    orderbook_df.set_index(['date', 'pair_symbol', 'quantity', 'exchange'],
                           inplace=True, drop=True)
    orderbook_df = orderbook_df.unstack(-1)

    for ob_types in [['ask', 'bid'], ['bid', 'ask']]:
        exchanges = context.exchanges.keys()[:]

        while len(exchanges) > 0:
            source_exchange = exchanges.pop(0)

            for target_exchange in exchanges:
                label = '{}_{}'.format(source_exchange, target_exchange)

                if ob_types[0] == 'ask':
                    orderbook_df['ask', label] = \
                        orderbook_df['bid'][target_exchange] - \
                        orderbook_df['ask'][source_exchange]

                    log.info(
                        'buying on {buy_exchange} (ask) selling on '
                        '{sell_exchange} (bid): '
                        '{sell_price} - {buy_price} = {profit}'.format(
                            buy_exchange=source_exchange,
                            sell_exchange=target_exchange,
                            buy_price=
                            orderbook_df['ask'][source_exchange].iloc[0],
                            sell_price=
                            orderbook_df['bid'][target_exchange].iloc[0],
                            profit=orderbook_df['ask', label].iloc[0]
                        )
                    )

                    percent_key = '{}_percent'.format(label)
                    orderbook_df['ask', percent_key] = \
                        orderbook_df['ask'][label] / \
                        orderbook_df['ask'][source_exchange] * 100

                    log.info(
                        'percent profit: {profit} / {buy_price} * 100 = '
                        '{result}'.format(
                            profit=orderbook_df['ask'][label].iloc[0],
                            buy_price=
                            orderbook_df['ask'][source_exchange].iloc[0],
                            result=orderbook_df['ask', percent_key].iloc[0]
                        )
                    )

                else:
                    orderbook_df['bid', label] = \
                        orderbook_df['bid'][source_exchange] - \
                        orderbook_df['ask'][target_exchange]

                    orderbook_df['bid', '{}_percent'.format(label)] = \
                        orderbook_df['bid'][label] / \
                        orderbook_df['ask'][target_exchange] * 100

    return orderbook_df


def send_email(df):
    bytes_to_write = df.to_csv(None).encode()
    return requests.post(
        "https://api.mailgun.net/v3/sandboxcec14dd65c2f4008952e1fad2e79ad19.mailgun.org/messages",
        auth=("api", "key-61013a4d1ff85ddd236a245a6967b72f"),
        files=[
            ("attachment", ("opportunity.csv", bytes_to_write))
        ],
        data={
            "from": "Conatus Alerts <postmaster@conatus.co>",
            "to": ["fredfortier@gmail.com"],
            "subject": "Arbitrage Opportunity",
            "text": "Conatus found the attached opportunity"})


def to_s3(df, subfolder, timestr):
    bytes_to_write = df.to_csv(None).encode()

    obj = s3.Object('conatus-public', 'orderbook-panel/{}/{}-{}.csv'.format(
        subfolder, timestr, algo_namespace
    ))
    obj.put(Body=bytes_to_write)


def create_price_panel(context, data):
    prices = []
    for pair_symbol in context.targets:
        spot_price = dict(
            pair_symbol=pair_symbol,
        )

        for exchange_name in context.exchanges:
            asset = symbol(pair_symbol, exchange_name)
            spot_price[exchange_name] = data.current(asset, 'price')

        prices.append(spot_price)

    price_df = pd.DataFrame(prices)
    price_df.set_index(['pair_symbol'], inplace=True, drop=True)

    exchanges = context.exchanges.keys()[:]
    while len(exchanges) > 0:
        source_exchange = exchanges.pop(0)

        for target_exchange in exchanges:
            label = '{}_{}'.format(source_exchange, target_exchange)
            price_df[label] = \
                price_df[target_exchange] - price_df[source_exchange]

            price_df['{}_percent'.format(label)] = \
                price_df[label] / price_df[source_exchange] * 100

    result = print_df(price_df)
    print(result)

    bytes_to_write = price_df.to_csv(None).encode()
    timestr = time.strftime('%Y%m%d-%H%M%S')

    obj = s3.Object('conatus-public', 'price-panel/{}-{}.csv'.format(
        timestr, algo_namespace
    ))
    obj.put(Body=bytes_to_write)


def create_orders(context, signals):
    log.info('found signal: {}'.format(signals))


def filter_entry_points(context, data):
    """
    Include filters which might stop us from entering positions.

    :param context:
    :param data:
    :return:
    """
    for pair_symbol in context.targets:
        for exchange in context.exchanges.values():
            asset = symbol(pair_symbol, exchange.name)


            # prices = data.history(
            #     asset,
            #     fields='price',
            #     bar_count=30,
            #     frequency='1m'
            # )
            # rsi = talib.RSI(prices.values, timeperiod=14)[-1]
            # print('got rsi: {}'.format(rsi))


def handle_data(context, data):
    exceptions = []
    try:
        # filter_entry_points(context, data)

        # create_price_panel(context, data)

        if context.sim_params.arena != 'backtest':
            create_orderbook_panel(context, data)

    except Exception as e:
        log.warn(e)
        exceptions.append(e)

    log.info('completed bar, exceptions: {}'.format(len(exceptions)))
    record(opportunities=context.num_opportunities)


def analyze(context, stats):
    print('the daily stats:\n{}'.format(get_pretty_stats(stats)))

    pass


# run_algorithm(
#     capital_base=250,
#     start=pd.to_datetime('2017-9-1', utc=True),
#     end=pd.to_datetime('2017-9-28', utc=True),
#     data_frequency='daily',
#     initialize=initialize,
#     handle_data=handle_data,
#     analyze=None,
#     exchange_name='poloniex,bitfinex,bittrex',
#     algo_namespace=algo_namespace,
#     base_currency='btc'
# )
run_algorithm(
    initialize=initialize,
    handle_data=handle_data,
    analyze=analyze,
    exchange_name='poloniex,bittrex',
    live=True,
    algo_namespace=algo_namespace,
    base_currency='btc',
    live_graph=False
)
