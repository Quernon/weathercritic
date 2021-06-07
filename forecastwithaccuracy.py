from forecast import Forecast

class ForecastWithAccuracy(Forecast):
    accuracy = {
        'rainfall': None,
        'temp': None
    }