from datetime import datetime, timedelta
from forecast import Forecast


class DayForecast(object):
    def __init__(self):
        self._id = datetime.today().strftime('%Y-%m-%d')
        self.bbc = Forecast()
        self.met = Forecast()
        self.actual = Forecast()

    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)

    def asDict(self):
        document = vars(self)
        return document

    def __repr__(self):
        return "<Test met:%s bbc:%s>" % (self.met, self.bbc)

    def __str__(self):
        return "From str method of Test: met is %s, bbc is %s" % (self.met, self.bbc)
