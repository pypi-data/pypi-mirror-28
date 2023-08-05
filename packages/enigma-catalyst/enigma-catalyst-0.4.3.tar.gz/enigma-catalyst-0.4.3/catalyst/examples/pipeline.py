from catalyst import run_algorithm
from catalyst.api import attach_pipeline, pipeline_output
from catalyst.exchange.exchange_pricing_loader import TradingPairPricing
from catalyst.pipeline import Pipeline, CustomFactor

import pandas as pd

from catalyst.pipeline.factors.equity import SimpleMovingAverage


# Custom factors are defined as a class object, outside of initialize or handle data.
# RecentReturns will calculate the returns for a security over the n-most recent days.
class RecentReturns(CustomFactor):
    # Set the default list of inputs as well as the default window_length.
    # Default values are used if the optional parameters are not specified.
    inputs = [TradingPairPricing.close]
    window_length = 10

    # Computes the returns over the last n days where n = window_length.
    # Any calculation can be performed here and is applied to all markets
    # in the universe.
    def compute(self, today, assets, out, close):
        out[:] = (close[-1] - close[0]) / close[0]


def initialize(context):
    my_pipe = make_pipeline()
    attach_pipeline(my_pipe, 'my_pipeline')

    context.first_frame = True


def make_pipeline():
    """
    Create our pipeline.
    """

    # 10-day close price average.
    mean_10 = SimpleMovingAverage(
        inputs=[TradingPairPricing.close],
        window_length=10,
    )

    # 30-day close price average.
    mean_30 = SimpleMovingAverage(
        inputs=[TradingPairPricing.close],
        window_length=30,
    )

    recent_returns = RecentReturns(
        inputs=[TradingPairPricing.close],
        window_length=14,
    )
    percent_difference = (mean_10 - mean_30) / mean_30

    # Filter to select securities to short.
    shorts = percent_difference.top(5)

    # Filter to select securities to long.
    longs = percent_difference.bottom(5)

    # Filter for all securities that we want to trade.
    securities_to_trade = (shorts | longs)

    pipe = Pipeline(
        columns={
            'longs': longs,
            'shorts': shorts,
            'recent_returns': recent_returns.top(5),
        },
        screen=(securities_to_trade),
    )

    return pipe


def handle_data(context, data):
    if context.first_frame:
        context.output = pipeline_output('my_pipeline')
        context.first_frame = False

    context.longs = context.output[context.output['longs']]
    print(context.longs.index)

    context.shorts = context.output[context.output['shorts']]
    print(context.shorts.index)

    context.recent_returns = context.output[context.output['recent_returns']]
    pass


if __name__ == '__main__':
    mode = 'backtest'

    if mode == 'backtest':
        run_algorithm(
            capital_base=1,
            initialize=initialize,
            handle_data=handle_data,
            analyze=None,
            exchange_name='poloniex',
            algo_namespace='simple_loop',
            base_currency='eth',
            data_frequency='minute',
            start=pd.to_datetime('2017-9-1', utc=True),
            end=pd.to_datetime('2017-12-25', utc=True),
        )
    else:
        run_algorithm(
            capital_base=1,
            initialize=initialize,
            handle_data=handle_data,
            analyze=None,
            exchange_name='binance',
            live=True,
            algo_namespace='simple_loop',
            base_currency='eth',
            live_graph=False,
            simulate_orders=True
        )
