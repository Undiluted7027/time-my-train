'''Gets trains'''
from re import I
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd


def get_trains_bw_stations(from_stn, to_stn, date_travel=0): # for indiarailinfo

    link = f"https://indiarailinfo.com/search/{from_stn}/0/{to_stn}"
    req = requests.get(link, headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
        })

    soup = BeautifulSoup(req.content, "lxml")
    element = soup.find_all("div", attrs={"style": "line-height:20px;"})
    trains = []
    for i in element:
        children = i.findChildren("div" , recursive=False)
        #print(children[1].text)

        if "Σ" not in children[2].text:
            
            t_num = children[0].text
            t_name = children[1].text
            days = children[14].text
            trains.append(children[1].text)
    
    return trains
        
#get_trains_bw_stations(1, 272)

def train_bw_stn_ry(from_stn_code, to_stn_code, date=0):
    link = f"https://www.railyatri.in/booking/trains-between-stations?from_code={from_stn_code}+&journey_date=30-05-2022&src=tbs&to_code={to_stn_code}+&user_id=-1653405993&user_token=61653405993&utm_source=tt_dwebhome_search"
    req = requests.get(link, headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"
    })
    soup = BeautifulSoup(req.content, "lxml")
    trains = [i.text.split(" ")[0] for i in soup.find_all("p", class_="TrainName")]
    # print(trains)
    return trains