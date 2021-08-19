from datetime import datetime, timedelta
from forecast import Forecast
# from forecastwithaccuracy import ForecastWithAccuracy


class DayForecast(object):
    def __init__(self):
        self._id = datetime.today().strftime('%Y-%m-%d')
        self.bbc = Forecast()
        self.met = Forecast()
        self.actual = Forecast()

    def __init__(self, dictionary):
        # print(dictionary)
        for k, v in dictionary.items():
            setattr(self, k, v)

    def asDict(self):
        # test_day_forecast = {}
        # test_day_forecast['_id'] = self._id
        # test_day_forecast.met = vars(self.met)
        # test_day_forecast.bbc = vars(self.bbc)
        # test_day_forecast.actual = vars(self.actual)
        document = vars(self)
        return document

    def __repr__(self):
        return "<Test met:%s bbc:%s>" % (self.met, self.bbc)

    def __str__(self):
        return "From str method of Test: met is %s, bbc is %s" % (self.met, self.bbc)
