from datetime import datetime, timedelta
from forecast import Forecast
# from forecastwithaccuracy import ForecastWithAccuracy

class DayForecast(object):
   def __init__(self):
     self._id = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
     self.bbc = Forecast()
     self.met = Forecast()
     self.actual = Forecast()