import logging

import pandas as pd
import numpy as np

from binance.client import Client

_logger = logging.getLogger(__name__)

def get_metadata(sid_map):
    client = Client("", "")
    metadata = pd.DataFrame(
        np.empty(
            len(sid_map),
            dtype=[
                ('symbol', 'str'),
                ('asset_name', 'str')
            ]
        )
    )
    for sid, symbol in sid_map:
        res = client.get_symbol_info(symbol)
        metadata.loc[sid, 'symbol'] = symbol
        metadata.loc[sid, 'asset_name'] = res['baseAsset']
        #metadata.loc[sid, 'start_date'] = pd.to_datetime(start_session) # this is a hack
    metadata['exchange'] = 'binance'
    return metadata

def _get_historical_klines(
        sid_map,
        start_session,
        end_session,
        cache,
        timeframe,
        show_progress):
    client = Client("", "")

    for sid, symbol in sid_map:
        key = symbol + '-' + timeframe
        if key not in cache:
            cache[key] = pd.DataFrame()
        while cache[key].empty or cache[key].index[-1] < end_session:
            cursor = start_session if cache[key].empty else cache[key].index[-1]
            _res = client.get_historical_klines(symbol, timeframe, str(cursor), str(end_session), 720)
            if not _res:
                break
            res = pd.DataFrame(_res).drop(columns=list(range(6,12)))
            res.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
            res['date'] = res['date'].map(lambda x: pd.Timestamp(x*1000000, tz='utc'))
            res.set_index('date', inplace=True)
            res.open = res.open.astype(np.float32)
            res.high = res.high.astype(np.float32)
            res.low = res.low.astype(np.float32)
            res.close = res.close.astype(np.float32)
            res.volume = res.volume.astype(np.float32)
            if not cache[key].empty:
                cache[key] = cache[key].drop(index=cache[key].index[-1])
            cache[key] = pd.concat([cache[key], res])
            if show_progress:
                _logger.debug("Fetched trades from {} to {}".format(cursor, end_session))
        yield sid, cache[key]

def get_historical_minute_klines(
        sid_map,
        start_session,
        end_session,
        cache,
        show_progress):
    return _get_historical_klines(sid_map, start_session, end_session, cache, '1m', show_progress)

def get_historical_daily_klines(
        sid_map,
        start_session,
        end_session,
        cache,
        show_progress):
    return _get_historical_klines(sid_map, start_session, end_session, cache, '1d', show_progress)
