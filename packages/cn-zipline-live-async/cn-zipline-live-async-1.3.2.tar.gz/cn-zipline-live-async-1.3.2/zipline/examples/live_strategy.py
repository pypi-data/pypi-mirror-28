# coding=utf-8

from zipline.api import order, record, symbol, schedule_function
from zipline.api import date_rules, get_datetime, cancel_order, time_rules
import platform


def rebalance(context, data):
    # order(context.smb, 100, limit_price=4.18)
    print("ordering")


def cancle_open_orders(context, data):
    for key, val in context.get_open_orders().items():
        for order in val:
            print(
                "cancel order {} for {}, amount {}, filled {}".format(order.id, order.sid, order.amount, order.filled))
            cancel_order(order.id)


def initialize(context):
    context.smb = symbol('000521')
    context.ordered = False
    # schedule_function(rebalance, date_rule=date_rules.every_day(), time_rule=time_rules.market_open(minutes=140))


def handle_data(context, data):
    hist = data.history(context.smb, bar_count=5, frequency='1m', fields='open')
    if not context.ordered:
        print("ordering")
        order(context.smb, 100, limit_price=5.00)
        context.ordered = True
    cancle_open_orders(context,data)
    print(hist)


if __name__ == '__main__':
    from zipline.utils.cli import Date
    from zipline.utils.run_algo import run_algorithm
    from zipline.gens.brokers.tdx_broker import TdxBroker
    import pandas as pd
    import os

    if platform.architecture()[0] == '32bit':
        client_uri = 'config.json'
    else:
        client_uri = "tcp://127.0.0.1:4242"
    broker = TdxBroker(client_uri)
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    realtime_bar_target = 'tmp/real-bar-{}'.format(str(pd.to_datetime('today').date()))
    state_filename = 'tmp/live-state'

    start = Date(tz='utc', as_timestamp=True).parser('2017-03-01')

    end = Date(tz='utc', as_timestamp=True).parser('2017-11-01')

    run_algorithm(start, end, initialize, 10e6, handle_data=handle_data, bundle='tdx',
                  trading_calendar='SHSZ', data_frequency="minute", output='out.pickle',
                  broker=broker, state_filename=state_filename, realtime_bar_target=realtime_bar_target)
