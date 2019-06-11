"""
Zipline bundle for Binance Exchange
"""
import pandas as pd

from trading_calendars import register_calendar

from .calendar import BinanceCalendar
from .api import (
        get_metadata,
        get_historical_minute_klines,
        get_historical_daily_klines
)

__author__ = "Ian MacKay"
__copyright__ = "Ian MacKay"
__license__ = "Apache v2"



def create_bundle(symbols, start=None, end=None):
    def ingest(
            environ,
            asset_db_writer,
            minute_bar_writer,
            daily_bar_writer,
            adjustment_writer,
            calendar,
            start_session,
            end_session,
            cache,
            show_progress,
            output_dir,
            start=start,
            end=end):
        if start is None:
            start = start_session
        if end is None:
            end = end_session
        sid_map = list(zip(range(len(symbols)), symbols))
        adjustment_writer.write()
        asset_db_writer.write(
                equities=get_metadata(sid_map),
                exchanges=pd.DataFrame(
                    data=[['binance', 'UTC']],
                    columns=['exchange', 'timezone'])
        )

        minute_bar_writer.write(
                get_historical_minute_klines(sid_map, start, end, cache, show_progress),
                show_progress=show_progress
        )

        daily_bar_writer.write(
                get_historical_daily_klines(sid_map, start, end, cache, show_progress),
                show_progress=show_progress
        )
    return ingest

register_calendar('BINANCE', BinanceCalendar())
