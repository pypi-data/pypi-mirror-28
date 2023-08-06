from fireant.slicer import (
    annually,
    daily,
    hourly,
    monthly,
    quarterly,
    weekly,
)
from pypika import (
    VerticaQuery,
    functions as fn,
    terms,
)
from .base import Database


class Trunc(terms.Function):
    """
    Wrapper for Vertica TRUNC function for truncating dates.
    """

    def __init__(self, field, date_format, alias=None):
        super(Trunc, self).__init__('TRUNC', field, date_format, alias=alias)
        # Setting the fields here means we can access the TRUNC args by name.
        self.field = field
        self.date_format = date_format
        self.alias = alias


class VerticaDatabase(Database):
    """
    Vertica client that uses the vertica_python driver.
    """
    # The pypika query class to use for constructing queries
    query_cls = VerticaQuery

    DATETIME_INTERVALS = {
        hourly: 'HH',
        daily: 'DD',
        weekly: 'IW',
        monthly: 'MM',
        quarterly: 'Q',
        annually: 'Y'
    }

    def __init__(self, host='localhost', port=5433, database='vertica', user='vertica', password=None,
                 read_timeout=None):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.read_timeout = read_timeout

    def connect(self):
        import vertica_python

        return vertica_python.connect(host=self.host, port=self.port, database=self.database,
                                      user=self.user, password=self.password,
                                      read_timeout=self.read_timeout)

    def trunc_date(self, field, interval):
        trunc_date_interval = self.DATETIME_INTERVALS.get(interval, 'DD')
        return Trunc(field, trunc_date_interval)

    def date_add(self, field, date_part, interval, align_weekday=False):
        shifted_date = fn.TimestampAdd(date_part, interval, field)

        if align_weekday:
            truncated = self.trunc_date(shifted_date, weekly)
            return fn.TimestampAdd(date_part, -interval, truncated)

        return shifted_date

    def totals(self, query, terms):
        return query.rollup(*terms)
