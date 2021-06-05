import threading

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def bbcweather():
    chorlton_url = "https://www.bbc.co.uk/weather/6691248"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    browser = webdriver.Chrome(options=chrome_options)

    browser.get(chorlton_url)
    soup = BeautifulSoup(browser.page_source,"html.parser")
    
    timeSlots = soup.find_all('div', class_="wr-time-slot-primary__title")
    bbcReport = []
    for slot in timeSlots:
        timeDetails = slot.findNext("div").findNext("div")
        description = timeDetails.find(class_="wr-weather-type__text").text
        temp = timeDetails.find(class_="wr-value--temperature--c").text
        rain = timeDetails.find(class_="wr-time-slot-primary__precipitation").text.replace("chance of precipitation", " chance of rain")
        wind = timeDetails.find(class_="wr-value--windspeed").text
        slotText = f'{slot.text}: {description}, {temp} {rain}, wind speed:{wind}\n'
        bbcReport.append(slotText)
        print(slotText)

if __name__ == "__main__":
    format = "%Y-%m-%d"
threading.Thread(target=bbcweather).start()
