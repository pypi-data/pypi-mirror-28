import json
import shutil
import tarfile
import tempfile

import os
import pandas as pd

import boto3
from catalyst.constants import EXCHANGE_CONFIG_URL
from catalyst.data.bundles.core import download_without_progress
from catalyst.exchange.exchange_bcolz import BcolzExchangeBarReader
from catalyst.exchange.utils.exchange_utils import save_exchange_config
from catalyst.exchange.utils.factory import get_exchange, find_exchanges
from catalyst.exchange.utils.serialization_utils import \
    ExchangeJSONDecoder
from catalyst.utils.paths import ensure_directory
from six.moves.urllib import request
from catalyst.assets._assets import TradingPair

s3 = boto3.resource('s3')

ROOT_PATH = '/Users/fredfortier/.catalyst/test'


def get_last_dt_from_file(exchange_name, symbol, freq):
    path = 'catalyst-bundles/exchange-{}/'.format(exchange_name)
    try:
        bucket = s3.Bucket('enigmaco')
        objs = s3.list_objects(
            Bucket='enigmaco',
            Prefix='{}{}-{}-{}'.format(
                path, exchange_name, freq, symbol
            )
        )['Contents']

        objs_m = [o['Key'].decode('utf-8') for o in objs]
        objs_m.sort()
        last_key = objs_m[-1]

        url = 'https://s3.amazonaws.com/enigmaco/{}'.format(last_key)
        bytes = download_without_progress(url)
        path = tempfile.mkdtemp()
        with tarfile.open('r', fileobj=bytes) as tar:
            tar.extractall(path)
        reader = BcolzExchangeBarReader(path)
        last_date = reader.last_available_dt.strftime('%Y-%m-%d')
        shutil.rmtree(path)

    except Exception as e:
        print('unable to find bundles or dates: {}'.format(e))
        last_date = 'N/A'

    return last_date


def update_config_from_bcolz(exchange):
    try:
        url = EXCHANGE_CONFIG_URL.format(exchange=exchange.name)
        handle = request.urlopen(url=url)
        config = json.load(handle, cls=ExchangeJSONDecoder)

        assets = []
        for asset_dict in config['assets']:
            asset = TradingPair(**asset_dict)
            assets.append(asset)

        config['assets'] = assets

    except Exception:
        config = None

    new_config = exchange.create_exchange_config()
    if config is not None:
        new_assets = list(set(new_config['assets']) - set(config['assets']))

        if len(new_assets) > 0:
            for asset in new_assets:
                asset.start_date = pd.Timestamp.utcnow()

                config['assets'].append(asset)

    else:
        config = new_config

    for asset in config['assets']:
        symbol = asset.symbol
        asset.set_end_date(
            get_last_dt_from_file(exchange.name, symbol, 'daily'),
            'daily'
        )
        asset.set_end_date(
            get_last_dt_from_file(exchange.name, symbol, 'minute'),
            'minute'
        )

    folder = os.path.join(ROOT_PATH, 'exchanges', exchange.name)
    ensure_directory(folder)

    filename = os.path.join(folder, 'config.json')
    save_exchange_config(exchange.name, config, filename)

    try:
        s3.upload_file(
            filename,
            'enigmaco',
            'catalyst-exchanges/{}/config.json'.format(exchange.name),
            ExtraArgs={'ACL': 'public-read', 'ContentType': 'application/json'}
        )
    except Exception as e:
        print('unable to upload file: {}'.format(e))


exchanges = find_exchanges()

for exchange in exchanges:
    update_config_from_bcolz(exchange)
