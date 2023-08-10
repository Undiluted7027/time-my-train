from turtle import end_fill
from urllib import request
from bs4 import BeautifulSoup
import requests, csv
import pandas as pd

def create_csv(soup_data, t_num):
    #table_body = station_table.find('tbody')
    heads = soup_data.find_all('th')
    rows = soup_data.find_all('tr')
    data = []
    data.append([head.text.strip() for head in heads])
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text for ele in cols]
        data.append([ele for ele in cols if ele!=None])
    data.remove([])
    #print(data)
    with open(f"{t_num}.csv", "w", newline='') as f:
         csv_file = csv.writer(f)
         csv_file.writerows(data)




def get_station_from_code():
    df = pd.read_csv("stations.csv")


#get_route(soup, 664, 741)


def create_route(from_stn_code, to_stn_code, via=[], dates=0):
    link = f"https://indiarailinfo.com/route/{from_stn_code}/{to_stn_code}?via={via}"
    req = requests.get(link, headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"
    })
    soup = BeautifulSoup(req.content, "lxml")
    stns = soup.find_all("td", class_="first-child")[2:]
    stations = [stn.text for stn in stns if "stations" not in stn.text]
    print(stations)
    return stations

create_route(745, 249)