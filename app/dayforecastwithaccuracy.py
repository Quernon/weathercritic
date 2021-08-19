from dayforecast import DayForecast
from forecastwithaccuracy import ForecastWithAccuracy


class DayForecastWithAccuracy(object):
    def __init__(self, dayForecast):
        self._id = dayForecast._id
        self.actual = dayForecast.actual
        self.met = ForecastWithAccuracy(dayForecast.met, dayForecast.actual)
        self.bbc = ForecastWithAccuracy(dayForecast.bbc, dayForecast.actual)

    def asDict(self):
        document = vars(self)
        document['met'] = vars(self.met)
        document['bbc'] = vars(self.bbc)

        return document
