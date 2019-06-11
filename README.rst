===========================
Binance Support for Zipline
===========================

At some point this may be valuable to someone.

Description
===========

I spent about a day on it only to find that zipline is a bit too restrictive in supporting anything other than freedom dollars.
Perhaps at some point I'll try to modify zipline to be more conducive for crypto, but since it's slow and seemingly written by idiots I would rather not.
An implementation in a different language would be highly preferable for my purposes. Python gives me a headache.

If you have a use for it,
Clone this repository and install with pip::

    pip install -e .
    pip install -r ./requirements.txt

Example
=======

In your zipline extension.py, add::

.. code:: python

    import pandas as pd
    from zipline_binance import create_bundle
    from zipline.data.bundles import register

    start = pd.Timestamp('2019-05-01', tz='utc')
    end = pd.Timestamp('2019-06-01', tz='utc')
    assets = ['IOTABTC']

    register(
        'binance',
        create_bundle(assets, start, end),
        calendar_name='BINANCE',
        minutes_per_day=24*60,
        start_session=start,
        end_session=end
    )
