# 12936 stations
from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_stations():
    stations = []
    i = 0
    station = []
    for k in range(12539, 12937):

        LINK = f'https://indiarailinfo.com/departures/{k}?date=undefined&stptype=1&'
        req = requests.get(LINK , headers = {
            "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36"
        })
        soup = BeautifulSoup(req.text, "html.parser")
        result = soup.find('div', class_="srhres newbg inline alt")
        station_text = result.div.text
        print(station_text)
        station = station_text[station_text.find("from")+5: station_text.find("(")]
        stations.append(station)
        
        print(k, station)
        with open("stations.txt", "a", encoding="utf-8") as f:
            dat = f"{k}, {station}\n"
            f.write(dat)
            
get_stations()