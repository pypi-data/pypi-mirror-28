# Copyright 2015 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from logbook import Logger
from numpy import (
    iinfo,
    uint32,
)

from catalyst.constants import LOG_LEVEL
from catalyst.data.us_equity_pricing import BcolzDailyBarReader
from catalyst.errors import NoFurtherDataError
from catalyst.exchange.utils.factory import get_exchange
from catalyst.lib.adjusted_array import AdjustedArray
from catalyst.pipeline.data import DataSet, Column
from catalyst.pipeline.loaders.base import PipelineLoader
from catalyst.utils.calendars import get_calendar
from catalyst.utils.numpy_utils import float64_dtype

UINT32_MAX = iinfo(uint32).max

log = Logger('ExchangePriceLoader', level=LOG_LEVEL)


class TradingPairPricing(DataSet):
    """
    Dataset representing daily trading prices and volumes.
    """
    open = Column(float64_dtype)
    high = Column(float64_dtype)
    low = Column(float64_dtype)
    close = Column(float64_dtype)
    volume = Column(float64_dtype)


class ExchangePricingLoader(PipelineLoader):
    """
    PipelineLoader for Crypto Pricing data

    Delegates loading of baselines and adjustments.
    """

    def __init__(self, data_frequency):

        cal = get_calendar('OPEN')

        if data_frequency == 'daily':
            reader = None
            all_sessions = cal.all_sessions

        elif data_frequency == 'minute':
            reader = None
            all_sessions = cal.all_minutes

        else:
            raise ValueError(
                'Invalid data frequency: {}'.format(data_frequency)
            )

        self.data_frequency = data_frequency
        self.raw_price_loader = reader
        self._columns = TradingPairPricing.columns
        self._all_sessions = all_sessions

    @classmethod
    def from_files(cls, pricing_path):
        """
        Create a loader from a bcolz equity pricing dir and a SQLite
        adjustments path.

        Parameters
        ----------
        pricing_path : str
            Path to a bcolz directory written by a BcolzDailyBarWriter.
        """
        return cls(
            BcolzDailyBarReader(pricing_path),
        )

    def load_adjusted_array(self, columns, dates, assets, mask):
        # load_adjusted_array is called with dates on which the user's algo
        # will be shown data, which means we need to return the data that would
        # be known at the start of each date.  We assume that the latest data
        # known on day N is the data from day (N - 1), so we shift all query
        # dates back by a day.
        start_date, end_date = _shift_dates(
            self._all_sessions, dates[0], dates[-1], shift=1,
        )
        colnames = [c.name for c in columns]

        if len(assets) == 0:
            raise ValueError(
                'Pipeline cannot load data with eligible assets.'
            )

        exchange_names = []
        for asset in assets:
            if asset.exchange not in exchange_names:
                exchange_names.append(asset.exchange)

        exchange = get_exchange(exchange_names[0])
        reader = exchange.bundle.get_reader(self.data_frequency)

        raw_arrays = reader.load_raw_arrays(
            colnames,
            start_date,
            end_date,
            assets,
        )

        out = {}
        for c, c_raw in zip(columns, raw_arrays):
            out[c] = AdjustedArray(
                c_raw.astype(c.dtype),
                mask,
                {},
                c.missing_value,
            )
        return out

    @property
    def columns(self):
        return self._columns


def _shift_dates(dates, start_date, end_date, shift):
    try:
        start = dates.get_loc(start_date)
    except KeyError:
        if start_date < dates[0]:
            raise NoFurtherDataError(
                msg=(
                    "Pipeline Query requested data starting on {query_start}, "
                    "but first known date is {calendar_start}"
                ).format(
                    query_start=str(start_date),
                    calendar_start=str(dates[0]),
                )
            )
        else:
            raise ValueError("Query start %s not in calendar" % start_date)

    # Make sure that shifting doesn't push us out of the calendar.
    if start < shift:
        raise NoFurtherDataError(
            msg=(
                "Pipeline Query requested data from {shift}"
                " days before {query_start}, but first known date is only "
                "{start} days earlier."
            ).format(shift=shift, query_start=start_date, start=start),
        )

    try:
        end = dates.get_loc(end_date)
    except KeyError:
        if end_date > dates[-1]:
            raise NoFurtherDataError(
                msg=(
                    "Pipeline Query requesting data up to {query_end}, "
                    "but last known date is {calendar_end}"
                ).format(
                    query_end=end_date,
                    calendar_end=dates[-1],
                )
            )
        else:
            raise ValueError("Query end %s not in calendar" % end_date)
    return dates[start - shift], dates[end - shift]
