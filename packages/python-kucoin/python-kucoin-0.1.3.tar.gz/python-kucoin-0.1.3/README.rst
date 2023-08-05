===============================
Welcome to python-kucoin v0.1.3
===============================

.. image:: https://img.shields.io/pypi/v/python-kucoin.svg
    :target: https://pypi.python.org/pypi/python-kucoin

.. image:: https://img.shields.io/pypi/l/python-kucoin.svg
    :target: https://pypi.python.org/pypi/python-kucoin

.. image:: https://img.shields.io/travis/sammchardy/python-kucoin.svg
    :target: https://travis-ci.org/sammchardy/python-kucoin

.. image:: https://img.shields.io/coveralls/sammchardy/python-kucoin.svg
    :target: https://coveralls.io/github/sammchardy/python-kucoin

.. image:: https://img.shields.io/pypi/wheel/python-kucoin.svg
    :target: https://pypi.python.org/pypi/python-kucoin

.. image:: https://img.shields.io/pypi/pyversions/python-kucoin.svg
    :target: https://pypi.python.org/pypi/python-kucoin

This is an unofficial Python wrapper for the `Kucoin exchanges REST API v1 <https://kucoinapidocs.docs.apiary.io/>`_. I am in no way affiliated with Kucoin, use at your own risk.

PyPi
  https://pypi.python.org/pypi/python-kucoin

Source code
  https://github.com/sammchardy/python-kucoin

Documentation
  https://python-kucoin.readthedocs.io/en/latest/

Blog with examples
  https://sammchardy.github.io


Features
--------

- Implementation of most REST endpoints, more coming soon.
- Simple handling of authentication
- Response exception handling
- Simple buy and sell order functions
- Helper function `get_total_balance` to get balance in fiat

Quick Start
-----------

Register an account with `Kucoin <https://www.kucoin.com/#/?r=E42cWB>`_.

`Generate an API Key <https://www.kucoin.com/#/user/setting/api>`_ and enable it.

.. code:: bash

    pip install python-kucoin


.. code:: python

    from kucoin.client import Client
    client = Client(api_key, api_secret)

    # get currencies
    currencies = client.get_currencies()

    # get market depth
    depth = client.get_order_book('KCS-BTC', limit=50)

    # get symbol klines
    from_time = 1507479171
    to_time = 1510278278
    klines = client.get_kline_data_tv(
        'KCS-BTC',
        Client.RESOLUTION_1MINUTE,
        from_time,
        to_time
    )

    # place a buy order
    transaction = client.create_buy_order('KCS-BTC', '0.01', '1000')

    # get list of active orders
    orders = client.get_active_orders('KCS-BTC')

For more `check out the documentation <https://python-kucoin.readthedocs.io/en/latest/>`_.

Donate
------

If this library helped you out feel free to donate.

- ETH: 0xD7a7fDdCfA687073d7cC93E9E51829a727f9fE70
- NEO: AVJB4ZgN7VgSUtArCt94y7ZYT6d5NDfpBo
- LTC: LPC5vw9ajR1YndE1hYVeo3kJ9LdHjcRCUZ
- BTC: 1Dknp6L6oRZrHDECRedihPzx2sSfmvEBys

Other Exchanges
---------------

If you use `Binance <https://www.binance.com/?ref=10099792>`_ check out my `python-binance <https://github.com/sammchardy/python-binance>`_ library.

If you use `Quoinex <https://accounts.quoinex.com/sign-up?affiliate=PAxghztC67615>`_
or `Qryptos <https://accounts.qryptos.com/sign-up?affiliate=PAxghztC67615>`_ check out my `python-quoine <https://github.com/sammchardy/python-quoine>`_ library.

If you use `IDEX <https://idex.market>`_ check out my `python-idex <https://github.com/sammchardy/python-idex>`_ library.

.. image:: https://analytics-pixel.appspot.com/UA-111417213-1/github/python-kucoin?pixel