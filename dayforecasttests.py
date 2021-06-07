from forecast import Forecast
import unittest
from dayforecast import DayForecast

class TestDayForecast(unittest.TestCase):

    def test_output(self):
        today = DayForecast()

        # go and get bbc data, update the day forecast
        today.bbc = Forecast();
        today.bbc.rainfallHourly = {
            7: 10,
            8: 11
        }
        today.bbc.tempHourly = {
            7: 15,
            8: 16
        }

        # go and get met data, update the day forecast
        today.met = Forecast();
        today.met.rainfallHourly = {
            7: 8,
            8: 9
        }
        today.met.tempHourly = {
            7: 13,
            8: 14
        }

        self.assertEqual(today.bbc.rainfallHourly[7], 10)
        self.assertEqual(today.bbc.tempHourly[7], 15)
        self.assertEqual(today.met.rainfallHourly[7], 8)
        self.assertEqual(today.met.tempHourly[7], 13)

        # eventually, get the actual forecast
        today.actual.rainfallHourly = {
            7: 0,
            8: 0
        }


if __name__ == '__main__':
    unittest.main()