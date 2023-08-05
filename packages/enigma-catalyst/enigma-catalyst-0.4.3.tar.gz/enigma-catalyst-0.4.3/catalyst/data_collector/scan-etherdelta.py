import os
from web3 import Web3, IPCProvider
import pandas as pd
import json
import numpy as np
from six.moves.urllib import request

pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

FIRST_BLOCK = 3154485
LAST_BLOCK = 4700810
INCREMENT_BLOCKS = 100
CONTRACT_ADDRESS = '0x8d12A197cB00D4747a1fe03395095ce2A5CC6819'

contract_json = request.urlopen(
    'https://raw.githubusercontent.com/etherdelta/etherdelta.github.io/master/smart_contract/etherdelta.sol.json'
).read()
json_interface = json.loads(contract_json)

definition_json = request.urlopen(
    'https://raw.githubusercontent.com/etherdelta/etherdelta.github.io/master/config/main.json'
).read()
definition = json.loads(definition_json)


def find_token(addr):
    return next(
        (token for token in definition['tokens'] if
         token['addr'].lower() == addr.lower()),
        dict(name=addr, addr=addr, decimals=18),
    )


def create_trade(event, block):
    args = event['args']
    trade = dict(
        token_get=args['tokenGet'],
        amount_get=np.float64(args['amountGet']),
        token_give=args['tokenGive'],
        amount_give=np.float64(args['amountGive']),
        address_get=args['get'],
        address_give=args['give'],
        block=event['blockNumber'],
        trade_dt=pd.to_datetime(block['timestamp'], unit='s', utc=True),
    )

    if trade['amount_get'] > 0:
        trade['price'] = trade['amount_give'] / trade['amount_get']

    else:
        trade['price'] = 0

    quote_token = find_token(trade['token_give'])
    trade['quote_currency'] = quote_token['name']
    trade['decimals'] = quote_token['decimals']

    base_token = find_token(trade['token_get'])
    trade['base_currency'] = base_token['name']

    if trade['quote_currency'] is not None and trade[
        'base_currency'] is not None:
        trade['symbol'] = '{}_{}'.format(trade['base_currency'].lower(),
                                         trade['quote_currency'].lower())

    return trade


userdir = '/Users/fredfortier'
w3 = Web3(IPCProvider('{}/.ethereum/geth.ipc'.format(userdir)))

token_contract = w3.eth.contract(
    abi=json_interface,
    address=CONTRACT_ADDRESS
)  # Type: Contract

blocks = np.arange(FIRST_BLOCK, LAST_BLOCK, INCREMENT_BLOCKS)
counter = dict()
for index, block in enumerate(blocks):
    try:
        next_block = blocks[index + 1] - 1
    except IndexError:
        print('ingestion complete at block {}'.format(block))
        break

    transfer_filter = token_contract.eventFilter(
        event_name='Trade',
        filter_params=dict(
            fromBlock=int(block),
            toBlock=int(next_block),
        )
    )
    trade_entries = transfer_filter.get_all_entries()

    # deposit_filter = token_contract.eventFilter(
    #     event_name='Deposit',
    #     filter_params=dict(
    #         fromBlock=int(block),
    #         toBlock=int(next_block),
    #     )
    # )
    # deposit_entries = deposit_filter.get_all_entries()
    #
    # withdraw_filter = token_contract.eventFilter(
    #     event_name='Trade',
    #     filter_params=dict(
    #         fromBlock=int(block),
    #         toBlock=int(next_block),
    #     )
    # )
    # withdraw_filter = withdraw_filter.get_all_entries()

    if trade_entries:
        trades = []
        for event in trade_entries:
            block = w3.eth.getBlock(event['blockNumber'])

            trade = create_trade(event, block)
            trades.append(trade)

        if not trades:
            continue

        decimals = trades[0]['decimals']

        df = pd.DataFrame(trades)
        df.set_index(['symbol', 'trade_dt'], inplace=True, drop=True)
        df.sort_index(inplace=True)

        print('block {}:\n{}'.format(event['blockNumber'], df.head()))

        symbols = df.index.get_level_values('symbol')
        for symbol in symbols:
            symbol_df = df.loc[(symbols == symbol)]  # Type: pd.DataFrame
            if symbol in counter:
                counter[symbol] += len(symbol_df.index)

            else:
                counter[symbol] = len(symbol_df.index)

            folder = os.path.join(
                userdir, '.catalyst-data', 'etherdelta', 'trades'
            )
            if not os.path.exists(folder):
                os.makedirs(folder)

            filename = os.path.join(
                folder, '{}.csv'.format(symbol)
            )
            if os.path.exists(filename):
                print_headers = False

            else:
                print_headers = True

            with open(filename, 'a') as f:
                symbol_df.to_csv(
                    path_or_buf=f,
                    header=print_headers,
                    float_format='%.{}f'.format(decimals),
                )

        totals_df = pd.Series(counter)
        totals_filename = os.path.join(folder, 'totals.csv')
        with open(totals_filename, 'w+') as f:
            totals_df.to_csv(f, header=True)

    else:
        print('no trades in range {}-{}'.format(block, next_block))
